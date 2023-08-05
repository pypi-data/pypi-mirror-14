
from hgsvn import ui
from hgsvn.errors import (
    EmptySVNLog
    , ExternalCommandFailed
    , RunCommandError
)
from hgsvn.shell import once_or_more, run_command

import os
import time
import calendar
import operator
import re

try:
    from xml.etree import cElementTree as ET
except ImportError:
    try:
        from xml.etree import ElementTree as ET
    except ImportError:
        try:
            import cElementTree as ET
        except ImportError:
            from elementtree import ElementTree as ET


svn_log_args = ['log', '--xml', '-v']
svn_info_args = ['info', '--xml']
svn_checkout_args = ['checkout', '-q']
svn_status_args = ['status', '--xml', '--ignore-externals']

_identity_table = "".join(map(chr, range(256)))
_forbidden_xml_chars = "".join(
    set(map(chr, range(32))) - set('\x09\x0A\x0D')
)

def run_svn(args=None, bulk_args=None, fail_if_stderr=False,
            mask_atsign=False):
    """
    Run an SVN command, returns the (bytes) output.
    """
    if mask_atsign:
        # The @ sign in Subversion revers to a pegged revision number.
        # SVN treats files with @ in the filename a bit special.
        # See: http://stackoverflow.com/questions/1985203
        for idx in range(len(args)):
            if "@" in args[idx] and args[idx][0] not in ("-", '"'):
                args[idx] = "%s@" % args[idx]
        if bulk_args:
            for idx in range(len(bulk_args)):
                if ("@" in bulk_args[idx]
                    and bulk_args[idx][0] not in ("-", '"')):
                    bulk_args[idx] = "%s@" % bulk_args[idx]
    return run_command("svn",
        args=args, bulk_args=bulk_args, fail_if_stderr=fail_if_stderr)

def strip_forbidden_xml_chars(xml_string):
    """
    Given an XML string, strips forbidden characters as per the XML spec.
    (these are all control characters except 0x9, 0xA and 0xD).
    """
    return xml_string.translate(_identity_table, _forbidden_xml_chars)


def svn_date_to_timestamp(svn_date):
    """
    Parse an SVN date as read from the XML output and return the corresponding
    timestamp.
    """
    # Strip microseconds and timezone (always UTC, hopefully)
    # XXX there are various ISO datetime parsing routines out there,
    # cf. http://seehuhn.de/comp/pdate
    date = svn_date.split('.', 2)[0]
    time_tuple = time.strptime(date, "%Y-%m-%dT%H:%M:%S")
    return calendar.timegm(time_tuple)

def parse_svn_info_xml(xml_string):
    """
    Parse the XML output from an "svn info" command and extract useful information
    as a dict.
    """
    d = {}
    xml_string = strip_forbidden_xml_chars(xml_string)
    tree = ET.fromstring(xml_string)
    entry = tree.find('.//entry')
    d['url'] = entry.find('url').text
    d['revision'] = int(entry.get('revision'))
    d['repos_url'] = tree.find('.//repository/root').text
    d['last_changed_rev'] = int(tree.find('.//commit').get('revision'))
    author_element = tree.find('.//commit/author')
    if author_element is not None:
        d['last_changed_author'] = author_element.text
    d['last_changed_date'] = svn_date_to_timestamp(tree.find('.//commit/date').text)
    return d

class svnlog_merge_entry():
    revno = -1
    entry = {}

def parse_svn_log_xml_entry(entry):
        d = {}
        d['revision'] = int(entry.get('revision'))
        # Some revisions don't have authors, most notably the first revision
        # in a repository.
        # logentry nodes targeting directories protected by path-based
        # authentication have no child nodes at all. We return an entry
        # in that case. Anyway, as it has no path entries, no further
        # processing will be made.
        author = entry.find('author')
        date = entry.find('date')
        msg = entry.find('msg')
        src_paths = entry.find('paths')
        # Issue 64 - modified to prevent crashes on svn log entries with "No author"
        d['author'] = author is not None and author.text or "No author"
        if date is not None:
            d['date'] = svn_date_to_timestamp(date.text)
        else:
            d['date'] = None
        d['message'] = msg is not None and msg.text or ""
        paths = d['changed_paths'] = []
        if not (src_paths is None):
            for path in src_paths.findall('.//path'):
                copyfrom_rev = path.get('copyfrom-rev')
                if copyfrom_rev:
                    copyfrom_rev = int(copyfrom_rev)
                paths.append({
                    'path': path.text,
                    'action': path.get('action'),
                    'copyfrom_path': path.get('copyfrom-path'),
                    'copyfrom_revision': copyfrom_rev,
                })

        ui.status("svnlog entry: rev=%d "%(d['revision']), level=ui.PARSE)
        merges = list();
        for rev in entry.findall('logentry'):
            revno = int(rev.get('revision'))
            if revno == d['revision']: continue
            revdef = svnlog_merge_entry()
            revdef.revno = revno
            ui.status("svnlog r%d merge r%d"%(d['revision'], revno), level=ui.DEBUG)
            revdef.entry = parse_svn_log_xml_entry(rev)
            merges.append(revdef)
            break
        if len(merges) <= 0:
            merges = None
        d['merges'] = merges
        return d

svnlog_revseq_no   = 0
svnlog_revseq_up   = 1
svnlog_revseq_down = -1

def svnlog_revseq(revstart, revend):
    if (revstart > revend):
        return svnlog_revseq_down
    elif (revstart < revend):
        return svnlog_revseq_up
    return svnlog_revseq_no

def parse_svn_log_xml(xml_string, strict_log_seq = True):
    """
    Parse the XML output from an "svn log" command and extract useful information
    as a list of dicts (one per log changeset).
    
    strict_log_seq  - no - no resisions order stricts
                    - up - revisions must flow incrising order
                    - down - revisions must flow decrising order
    """
    l = []
    xml_string = strip_forbidden_xml_chars(xml_string)
    tree = ET.fromstring(xml_string)
    last_rev = -1
    use_strict = 0;
    entry = tree.find('logentry')
    
    while not(entry is None):
        d = parse_svn_log_xml_entry(entry);
        now_rev = int(d['revision'])
        if (strict_log_seq):
            if use_strict == 0:
                if last_rev >= 0:
                    use_strict = (now_rev - last_rev)
            else:
                isup = (use_strict > 0) and (last_rev < now_rev)
                isdn = (use_strict < 0) and (last_rev > now_rev)
                if not (isup or isdn):
                    ui.status("svn log broken revisions sequence: %d after %d"%(d['revision'], last_rev), level=ui.WARNING);
                    if ui.is_debug():
                        ui.status("xml dump:\n %s"%xml_string, level = ui.DEBUG, truncate = False)
                    break
        l.append(d)
        last_rev = now_rev
        tree.remove(entry)
        entry = tree.find('logentry')
    return l

def parse_svn_status_xml_entry(tree, base_dir=None, ignore_externals=False):
    isSVNPre180 = False;
    l = []
    for entry in tree.findall('.//entry'):
        d = {}
        path = entry.get('path')
        if path is None: continue
        if base_dir is not None:
            ui.status("svn status path:%s by entry:%s"%(base_dir, path), level=ui.PARSE)
            if not isSVNPre180:
                if os.path.normcase(path).startswith(base_dir):
                    ui.status("svn status check version: pre 1.8.0 ", level=ui.PARSE)
                    isSVNPre180 = True
                    path = path[len(base_dir):].lstrip('/\\')
                else:
                    ui.status("svn status check version: looks > 1.8.0 ", level=ui.PARSE)
                    base_dir = None
            else:
                assert os.path.normcase(path).startswith(base_dir)
                path = path[len(base_dir):].lstrip('/\\')
        d['path'] = path
        wc_status = entry.find('wc-status')
        if wc_status is None:
            continue
        if wc_status.get('item') == 'external':
            if ignore_externals:
                continue
            d['type'] = 'external'
        elif wc_status.get('item') == 'replaced':
            d['type'] = 'normal'
        elif wc_status.get('revision') is not None:
            d['type'] = 'normal'
        else:
            d['type'] = 'unversioned'
        if wc_status.get('tree-conflicted') is None:
            d['status'] = wc_status.get('item')
        else:
            d['status'] = 'conflicted'
        d['props'] = wc_status.get('props')
        if d is not None:
            l.append(d)
            ui.status("svn status have:%s"%d, level=ui.PARSE)
    return l

def parse_svn_status_xml(xml_string, base_dir=None, ignore_externals=False):
    """
    Parse the XML output from an "svn status" command and extract useful info
    as a list of dicts (one per status entry).
    """
    if base_dir:
        base_dir = os.path.normcase(base_dir)
    l = []
    xml_string = strip_forbidden_xml_chars(xml_string)
    tree = ET.fromstring(xml_string)
    for target in tree.findall('.//target'):
        path = target.get('path')
        if path is not None:
            if base_dir is not None:
                ui.status("svn status target path:%s of base %s"%(path, base_dir), level=ui.PARSE)
                path = os.path.normcase(path)
                assert path.startswith(base_dir)
                #path = path[len(base_dir):].lstrip('/\\')
                ui.status("svn status target subpath as:\'%s\'"%(path), level=ui.PARSE)
                if len(path) == 0:
                    path = None
        else:
            path=base_dir
        subl = parse_svn_status_xml_entry(target, path, ignore_externals)
        if subl is not None:
            l.extend(subl)
        tree.remove(target)

    subl = parse_svn_status_xml_entry(tree, base_dir, ignore_externals)
    if subl is not None:
        l.extend(subl)

    return l

def get_svn_info(svn_url_or_wc, rev_number=None):
    """
    Get SVN information for the given URL or working copy, with an optionally
    specified revision number.
    Returns a dict as created by parse_svn_info_xml().
    """
    if rev_number is not None:
        args = ['-r', rev_number]
    else:
        args = []
    xml_string = run_svn(svn_info_args + args + [svn_url_or_wc],
        fail_if_stderr=True)
    return parse_svn_info_xml(xml_string)

def svn_checkout(svn_url, checkout_dir, rev_number=None):
    """
    Checkout the given URL at an optional revision number.
    """
    args = []
    if rev_number is not None:
        args += ['-r', rev_number]
    args += [svn_url, checkout_dir]
    return run_svn(svn_checkout_args + args)

def run_svn_log_restricted_merges(svn_url, rev_start, rev_end, limit, stop_on_copy=False):
    """
    Fetch up to 'limit' SVN log entries between the given revisions.
    """
    if stop_on_copy:
        args = ['--stop-on-copy']
    else:
        args = []
    reslog = None
    args += ['-r','%s:%s' % (rev_start, rev_end), '--limit', limit, svn_url]
    xml_string = run_svn(svn_log_args + args)
    reslog = parse_svn_log_xml(xml_string)
    for element in (reslog):
        rev = element['revision']
        args = ['-r','%s' % rev, '-g', svn_url]
        xml_string = run_svn(svn_log_args + args)
        emerges = parse_svn_log_xml(xml_string) #, strict_log_seq = False
        if len(emerges) != 1:
            raise
        element['merges'] = emerges[0]['merges']
    return reslog

def run_svn_log(svn_url, rev_start, rev_end, limit, stop_on_copy=False):
    """
    Fetch up to 'limit' SVN log entries between the given revisions.
    """
    if stop_on_copy:
        args = ['--stop-on-copy']
    else:
        args = []
    reslog = None
    try:
            args += ['-r','%s:%s' % (rev_start, rev_end), '-g', '--limit', limit, svn_url]
            xml_string = run_svn(svn_log_args + args)
            reslog = parse_svn_log_xml(xml_string)
    except (RunCommandError), e:
            if e.err_msg.find("truncated HTTP response body") <= 0:
                ui.status("svn log failed:%s" % e.msg(noout=True) , level= ui.ERROR)
                raise
            ui.status("svn log failed, try to fetch in safer way", level= ui.VERBOSE)
            reslog = run_svn_log_restricted_merges(svn_url, rev_start, rev_end, limit, stop_on_copy)
    return reslog

def get_svn_status(svn_wc, quiet=False):
    """
    Get SVN status information about the given working copy.
    """
    # Ensure proper stripping by canonicalizing the path
    svn_wc = os.path.abspath(svn_wc)
    args = [svn_wc]
    if quiet:
        args += ['-q']
    else:
        args += ['-v']
    xml_string = run_svn(svn_status_args + args)
    return parse_svn_status_xml(xml_string, svn_wc, ignore_externals=True)

def svn_is_clean(svn_wc):
    svn_wc = os.path.abspath(svn_wc)
    changes = run_svn(['st', svn_wc ,'-q'])
    changes = changes.strip()
    ui.status("svn status is %s changes", len(changes), level=ui.VERBOSE);
    return (len(changes) <= 0)

def get_svn_versioned_files(svn_wc):
    """
    Get the list of versioned files in the SVN working copy.
    """
    contents = []
    for e in get_svn_status(svn_wc):
        if e['path'] and e['type'] == 'normal':
            contents.append(e['path'])
    return contents


def get_one_svn_log_entry(svn_url, rev_start, rev_end, stop_on_copy=False):
    """
    Get the first SVN log entry in the requested revision range.
    """
    entries = run_svn_log(svn_url, rev_start, rev_end, 1, stop_on_copy)
    if entries:
        return entries[0]
    raise EmptySVNLog("No SVN log for %s between revisions %s and %s" %
        (svn_url, rev_start, rev_end))


def get_first_svn_log_entry(svn_url, rev_start, rev_end):
    """
    Get the first log entry after (or at) the given revision number in an SVN branch.
    By default the revision number is set to 0, which will give you the log
    entry corresponding to the branch creaction.

    NOTE: to know whether the branch creation corresponds to an SVN import or
    a copy from another branch, inspect elements of the 'changed_paths' entry
    in the returned dictionary.
    """
    return get_one_svn_log_entry(svn_url, rev_start, rev_end, stop_on_copy=True)

def get_last_svn_log_entry(svn_url, rev_start, rev_end):
    """
    Get the last log entry before (or at) the given revision number in an SVN branch.
    By default the revision number is set to HEAD, which will give you the log
    entry corresponding to the latest commit in branch.
    """
    return get_one_svn_log_entry(svn_url, rev_end, rev_start, stop_on_copy=True)


log_duration_threshold = 10.0
log_min_chunk_length = 10

def iter_svn_log_entries(svn_url, first_rev, last_rev, retry):
    """
    Iterate over SVN log entries between first_rev and last_rev.

    This function features chunked log fetching so that it isn't too nasty
    to the SVN server if many entries are requested.
    """
    cur_rev = first_rev
    chunk_length = log_min_chunk_length
    first_run = True
    while last_rev == "HEAD" or cur_rev <= last_rev:
        start_t = time.time()
        stop_rev = min(last_rev, cur_rev + chunk_length)
        ui.status("Fetching %s SVN log entries starting from revision %d...",
                  chunk_length, cur_rev, level=ui.VERBOSE)
        entries = once_or_more("Fetching SVN log", retry, run_svn_log, svn_url,
                               cur_rev, last_rev, chunk_length)
        duration = time.time() - start_t
        if not first_run:
            # skip first revision on subsequent runs, as it is overlapped
            entries.pop(0)
        first_run = False
        if not entries:
            break
        for e in entries:
            if e['revision'] > last_rev:
                break
            yield e
        if e['revision'] >= last_rev:
            break
        cur_rev = e['revision']
        # Adapt chunk length based on measured request duration
        if duration < log_duration_threshold:
            chunk_length = int(chunk_length * 2.0)
        elif duration > log_duration_threshold * 2:
            chunk_length = max(log_min_chunk_length, int(chunk_length / 2.0))


_svn_client_version = None

def get_svn_client_version():
    """Returns the SVN client version as a tuple.

    The returned tuple only contains numbers, non-digits in version string are
    silently ignored.
    """
    global _svn_client_version
    if _svn_client_version is None:
        raw = run_svn(['--version', '-q']).strip()
        _svn_client_version = tuple(map(int, [x for x in raw.split('.')
                                              if x.isdigit()]))
    return _svn_client_version

def svn_cleanup():
    args = ["cleanup"]
    return run_svn(args)

def svn_resolve_all():
    args = ["resolve","-R","--non-interactive","--accept=working","."]
    return run_svn(args)

def svn_revert_all():
    args = ["revert","-R","--non-interactive","."]
    try:
        run_svn(args)
    except (ExternalCommandFailed), e:
        if str(e).find("Run 'svn cleanup'") <= 0:
            raise
        svn_cleanup()
        run_svn(args)
    return 

def svn_switch_to(svn_base, rev_number = None, clean = False, ignore_ancetry=False, propagate_rev = False):
    # propagate_rev - provides smart handle of situation when rev_number is origin of desired branch base, and branch is pure, 
    #       so that we can take
    args = ["switch","--non-interactive","--force"]
    if ignore_ancetry:
        args += ["--ignore-ancestry"]
    if rev_number is not None:
        svn_base += '@%s'%rev_number
    args += [svn_base]
    ui.status("switching to %s" % svn_base, level=ui.DEBUG)
    if clean:
        # switching is some like merge - on modified working copy try merges changes and got conflicts
        # therefor revert all before switch for prepare one
        svn_revert_all()
    try:
        run_svn(args)
    except (ExternalCommandFailed), e:
        delpath = re.search(r"Can't remove directory '(?P<delpath>\S+)'", str(e))
        nopath = re.search(r" path not found'(?P<delpath>\S+)'", str(e))
        if not (delpath is None):
            #when switchwith externals svn can confuse on removing absent directories
            if str(e).find("Removed external") <= 0:
                raise
            
            failepath = nestpath.group("delpath")
            ui.status("try switch again after remove absent dir %s" % failepath, level=ui.VERBOSE)
            run_svn(args)
        elif propagate_rev and (not (nopath is None)):
            #try to propagate rev_number to branch base if can
            branch_info = svn_branch_revset()
            (rev_base, rev_origin, rev_head) = branch_info.eval_path(svn_base)
            if (rev_base == rev_head) and (rev_origin == rev_number):
                basehgid = get_hg_cset_of_svn(rev_base)
                if (len(basehgid) == 0):
                    ui.status('branch svn:%s@%s used as candidate for its origin %s'%(svn_base, rev_base, rev_origin));
                    origin_hgid = get_hg_cset_of_svn(rev_number)
                    hg_rev_tag_by_svn(origin_hgid, rev_base)
                    svn_switch_to(svn_base, rev_base, clean, ignore_ancetry, False)
        else:
            raise

class svn_branch_revset(object):
    #this class describes svn-branch
    headrev      = None
    baserev      = None
    source       = None
    srcrev       = None
    path         = None

    def __repr__(self):
        return "svn branch: head:%s  base:%s path:%s sourced from %s"%(self.headrev, self.baserev, self.path, self.source)
            
    def eval_path(self, svn_base):
        self.path = svn_base
        self.source = None
        try:
            base   = get_first_svn_log_entry(svn_base, 0, 'HEAD')
        except (RunCommandError), e:
            if e.err_have("File not found") or e.err_have("path not found"):
                ui.status("svn looks have no branch %s" % svn_base) # , level= ui.ERROR
                base = None
            else:
                raise
        if base is None:
            self.baserev = None
            self.headrev = None
            return self.baserev, self.source, self.headrev
        head   = get_last_svn_log_entry(svn_base, 0, 'HEAD')
        self.baserev = base['revision']
        self.headrev = head['revision']
        paths = base['changed_paths']
        if len(paths) > 0:
            path = paths[0]
            self.source = path['copyfrom_path']
            self.srcrev = path['copyfrom_revision']
        else:
            ui.status("cant determine branch %s origin source"%svn_base)
        return self.baserev, self.source, self.headrev
    
    #true if branch is just a plain copy on another without any evolution
    def is_clean(self):
        if (self.baserev != self.headrev):
            return False
        if (self.source is None):
            return False
        return True

def svn_branch_empty(svn_base):
    entryes = run_svn_log(svn_base, 0, 'HEAD', 2, stop_on_copy=True)
    if len(entryes) > 1:
        return False
    if len(entryes) == 0:
        return True
    base = entryes[0]
    # the 1st revision can only have 1 path entry - add branch folder
    if (len(base['changed_paths']) > 1):
        return False
    if not(base['merges'] is None):
        return False
    return True

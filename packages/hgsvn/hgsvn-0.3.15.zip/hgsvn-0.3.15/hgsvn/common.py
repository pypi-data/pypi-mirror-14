from hgsvn import ui
from hgsvn.ui import is_debug
from hgsvn.errors import ExternalCommandFailed, HgSVNError, RunCommandError
from hgsvn.shell import once_or_more
from hgsvn.hgclient import run_hg
from hgsvn.svnclient import ( svn_branch_revset
    , run_svn
    , svn_switch_to
    , svn_is_clean
    )

import os
import locale
from datetime import datetime
import time
from subprocess import Popen, PIPE, STDOUT
import shutil
import stat
import sys
import traceback
import codecs
import fileinput
import re

try:
    import commands
except ImportError:
    commands = None

class _SimpleFileLock(object):

    def __init__(self, filename, timeout=None):
        self.file = filename
        self.lock()

    def lock(self):
        if os.path.exists(self.file):
            raise LockHeld("Lock file exists.")
        open(self.file, "wb").close()

    def release(self):
        if os.path.exists(self.file):
            os.remove(self.file)


class _LockHeld(Exception):
    pass


# We import the lock logic from Mercurial if it is available, and fall back
# to a dummy (always successful) lock if not.
try:
    from mercurial.lock import lock as _lock
    try:
        from mercurial.error import LockHeld
    except ImportError:
        # LockHeld was defined in mercurial.lock in Mercurial < 1.2
        from mercurial.lock import LockHeld

except ImportError:
    _lock = _SimpleFileLock
    LockHeld = _LockHeld


hgsvn_private_dir = ".hgsvn"
hgsvn_lock_file = "lock"
hgsvn_branchmap_file = "branches.map"
hgsvn_svnignore_file = ".svnignore"

#this maps svn path as key to hg_branch
hgsvn_branchmap = dict()
hgsvn_branchmap_options = "uao"
svn_ignores = []

if "SVN_ASP_DOT_NET_HACK" in os.environ:
    svn_private_dir = "_svn"
else:
    svn_private_dir = '.svn'

hg_commit_prefix = "[svn r%d] "
# This seems sufficient for excluding all .svn (sub)directories
hg_exclude_options = ["-X", svn_private_dir, "-X", "**/%s" % svn_private_dir]

def skip_dirs(paths, basedir="."):
    """
    Skip all directories from path list, including symbolic links to real dirs.
    """
    # NOTE: both tests are necessary (Cameron Hutchison's patch for symbolic
    # links to directories)
    return [p for p in paths
        if not os.path.isdir(os.path.join(basedir, p))
        or os.path.islink(os.path.join(basedir, p))]


def hg_commit_from_svn_log_entry(entry, files=None):
    """
    Given an SVN log entry and an optional sequence of files, turn it into
    an appropriate hg changeset on top of the current branch.
    """
    # This will use the local timezone for displaying commit times
    timestamp = int(entry['date'])
    hg_date = str(datetime.fromtimestamp(timestamp))
    # Uncomment this one one if you prefer UTC commit times
    #hg_date = "%d 0" % timestamp
    message = (hg_commit_prefix % entry['revision']) + entry['message'].lstrip()
    commit_file = None
    
    if files is None:
        if ui.is_debug():
            #if no commit all changes, so show what is to commit
            args = ["st", "-armC"]
            out = run_hg(args, output_is_locale_encoding=True)
            ui.status(out, level=ui.DEBUG)
        
    try:
        commit_file = os.path.join(hgsvn_private_dir,
            "commit-%r.txt" % entry['revision'])
        f = open(commit_file, "wb")
        f.write(message.encode('utf-8'))
        f.close()
        msg_options = ["--encoding","utf-8","-l", commit_file]
        # the -m will now work on windows with utf-8 encoding argument
        # the CreateProcess win32api convert bytes to uicode by locale codepage
        # msg.encode('utf-8').decode('cp932').encode('cp932').decode('utf-8')
        options = ["ci"] + msg_options + ["-d", hg_date]
        if entry['author']:
            options.extend(["-u", entry['author']])
        if files:
            run_hg(options, files)
        else:
            run_hg(options)
    except ExternalCommandFailed:
        # When nothing changed on-disk (can happen if an SVN revision only
        # modifies properties of files, not their contents), hg ci will fail
        # with status code 1 (and stderr "nothing changed")
        if run_hg(['st', '-mard'], output_is_locale_encoding=True).strip():
            raise
    finally:
        if commit_file and os.path.exists(commit_file):
            os.remove(commit_file)
    svnrev = entry['revision']
    try:
        hg_tag_svn_rev(svnrev)
    except (RunCommandError), e:
      if e.err_have("tag") and e.err_have("already exists"):
        branch = hg_branch_of_work()
        have_taged_rev = get_hg_cset_of_svn(svnrev, branch)
        if (not (have_taged_rev is None)) and (len(have_taged_rev) > 0) :
            raise
        ui.status("svn.%s alredy have imports at another branch %s, so tag it with branch %s suffix"%(svnrev, have_taged_rev , branch), level=ui.WARNING);
        try:
            hg_tag_svn_mark( "%d.%s"%(svnrev,branch) )
        except:
            last_rev = get_svn_rev_from_hg()
            if last_rev != svnrev:
                run_hg(["rollback"])
                raise
      else:
        # Rollback the transaction.
        last_rev = get_svn_rev_from_hg()
        if last_rev != svnrev:
            ui.status("hgpull.tag commited: have %s need %s"%(last_rev, svnrev), level = ui.ERROR)
            run_hg(["verify"])
            try:
                hg_tag_svn_rev(svnrev)
            except:
                # looks like 
                last_rev = get_svn_rev_from_hg()
                if last_rev != svnrev:
                    run_hg(["rollback"])
                    raise

def hg_tag_svn_rev(rev_number):
    """
    Put a local hg tag according to the SVN revision.
    """
    run_hg(["tag", "-l", "svn.%d" % rev_number])

def hg_tag_svn_mark(rev_tag):
    """
    Put a local hg tag according to the SVN revision.
    same as hg_tag_svn_rev, but accept string tag name, not stricted ti digit
    """
    run_hg(["tag", "-l", "svn.%s" % rev_tag])

    
def hg_rev_tag_by_svn(hgrev, rev_number):
    """
    Put a local hg tag according to the SVN revision.
    """
    run_hg(["tag", "-r", hgrev, "-l", "svn.%d" % rev_number])

def get_svn_revs_from_tags(tags):
    revs = [int(tag[4:]) for tag in tags if tag.startswith('svn.')]
    # An hg changeset can map onto several SVN revisions, for example if a
    # revision only changed SVN properties.
    return revs
    
def get_svn_rev_from_tags(tags):
    revs = [int(tag[4:]) for tag in tags if tag.startswith('svn.')]
    # An hg changeset can map onto several SVN revisions, for example if a
    # revision only changed SVN properties.
    if revs:
        return max(revs)
    return None

def strip_hg_rev(rev_string):
    """
    Given a string identifying an hg revision, return a string identifying the
    same hg revision and suitable for revrange syntax (r1:r2).
    """
    if ":" in rev_string:
        return rev_string.split(":", 1)[0].strip()
    return rev_string.strip()

def strip_hg_revid(rev_string):
    """
    Given a string identifying an hg revision, return a string identifying the
    same hg revision and suitable for revrange syntax (r1:r2).
    """
    if ":" in rev_string:
        return rev_string.split(":", 2)[1].strip()
    return rev_string.strip()

def same_hg_rev(hg_cset, rev):
    if ":" in hg_cset:
        id = hg_cset.split(":", 2)
        if id[0].strip() == rev:
            return True
        if id[1].strip() == rev:
            return True
        return False
    else:
        return hg_cset == rev

def get_hg_cset(rev_string, branch = None):
    """
    Given a string identifying an hg revision, get the canonical changeset ID.
    """
    args = ["log", "--template", r"{rev}:{node|short}", "-r", rev_string]
    if  not(branch is None):
        args.extend(['-b', branch])
    return run_hg(args).strip()

def get_hg_current_cset():
    """
    Given a string identifying an current hg revision, get the canonical changeset ID.
    """
    args = ["id", "-n", "-i"]
    out = run_hg(args).strip().split(" ",2)
    return "%s:%s"%(out[1], out[0])

def tag_of_svn(svnrev):
    return "svn.%d"%svnrev

def get_hg_cset_of_svn(svnrev, branch = None):
    svntag = tag_of_svn(svnrev)
    return get_hg_cset(svntag, branch)

def get_hg_revs(rev_string):
    """
    Given a string identifying an hg revision, get the canonical changeset ID.
    """
    args = ["log", "--template", r"{node|short}\n", "-r", rev_string]
    return run_hg(args).strip()

def map_svn_rev_to_hg(svn_rev, hg_rev="tip", local=False, force = False):
    """
    Record the mapping from an SVN revision number and an hg revision (default "tip").
    """
    args = ["tag"]
    if local:
        args.append("-l")
    if force:
        args.append("-f")
    args.extend(["-r", strip_hg_rev(hg_rev), "svn.%d" % svn_rev])
    run_hg(args)

def get_svn_rev_from_hg( rev_string=None):
    """
    Get the current SVN revision as reflected by the hg working copy,
    or None if no match found.
    """
    if rev_string is None:
        tags = run_hg(['parents', '--template', '{tags}']).strip().split()
    else:
        tags = run_hg(["log", "--template", r"{tags}" , "-r", rev_string]).strip().split()
    return get_svn_rev_from_tags(tags)

class sync_rev_stat(object):
    svnrev      = None
    hgrev       = None
    svn_src     = None
    svn_base    = None

    def __repr__(self):
        return "synched svn:%s ; hg: %s ; svnbase:%s"%(self.svnrev, self.hgrev, self.svn_src)
    
def get_svn_rev_of_hgbranch( branch = "default"):
    """
    Get the current SVN revision as reflected by the hg working copy,
    or None if no match found.
    """
    fromver = "tip"
    ui.status("get_svn_rev_of_hgbranch: branch %s"%branch, level = ui.PARSE)
    res = sync_rev_stat()
    while True:
        try:
            logtags = run_hg(["log", "--template", r"{rev}:{node|short};{tags}\n" , "-b", branch, '-r %s:0 and tag()'%fromver, "-l 16"])
        except ExternalCommandFailed, err:
            #possibly the branch is just started and not yet pulled
            ui.status("branch %s looks absent!", branch, level = ui.VERBOSE);
            return res
        ui.status("get_svn_rev_of_hgbranch:%s"%logtags, level = ui.DEBUG)
        if len(logtags) == 0 : break
        loglines = logtags.strip().splitlines()
        for info in loglines:
            hgrev,tags = re.split(";", info)
            fromver = int(strip_hg_rev(hgrev))-1
            tagslist = tags.split()
            svnrev = get_svn_rev_from_tags(tagslist)
            if svnrev:
                ui.status("branch %s use hg:%s svn:%s"%(branch, hgrev, svnrev), level = ui.DEBUG);
                res.svnrev  = svnrev
                res.hgrev   = hgrev
                return res
            if fromver < 0:
                ui.status("branch %s looks empty!" % branch, level = ui.VERBOSE);
                return res
                
    #possibly the branch is just started and not yet pushed, so try to find ones hg-base, 
    #   and if it is alredy pushed treat it as branch sync-point
    logtags = run_hg(["log", "--template", r"{rev}:{node|short}\n" , "-r", 'first(branch(%s))'%branch, "-l", "16"])
    if len(logtags) == 0 :
        ui.status("hgbranch:%s empty - what a ??"%branch, level = ui.VERBOSE)
        return res
    ui.status("hgbranch:%s no synced"%branch, level = ui.VERBOSE)
    hgrevs = logtags.strip().splitlines()
    fromver = hgrevs[0]
    res.hgrev = fromver
    logtags = run_hg(["log", "--template", r"{rev}:{node|short};{tags}\n" , "-r", 'parents(%s)'%fromver])
    loglines = logtags.strip().splitlines()
    if (len(loglines) == 1):
            info = loglines[0]
            hgrev,tags = re.split(";",info)
            fromver = strip_hg_rev(hgrev)
            tagslist = tags.split()
            res.hgrev   = hgrev
            #need check branch of evaluated base svn rev - wich is on root-hg branch
            svnrevs = get_svn_revs_from_tags(tagslist)
            svnrev = None
            if svnrevs:
                #some svn branches started here, need to find if some one is origin of branch
                ui.status("hg:%s is originated from hgrev %s, check if it have alredy svn-branch started"%(branch,fromver))
                svn_origin = svn_branch_revset()
                svn_path = svn_base_of_branch(branch)
                svn_origin.eval_path('^'+svn_path)
                if (svn_origin.source is None) or (svn_origin.baserev is None):
                    #target svn-branch empty or absent, origin should be copyed there. so report that svn is none
                    svnrev = None
                elif svn_origin.is_clean():
                    res.svn_base = svn_origin.baserev
                    #check that svn_branch originated from hg-from
                    if svn_origin.baserev in svnrevs:
                        svnrev = svn_origin.baserev
                    elif svn_origin.srcrev in svnrevs:
                        #originates from the right place, so just declare that no synced
                        ui.status("hg:%s is originated from hgrev %s, wich synced with svn, possibly need to declare sync tag?"%(branch,fromver))
                        res.svn_src = svn_origin.srcrev
                        #svnrev = res.svn_src
                    else:
                        ui.status("hg:%s is originated from hgrev %s, wich miss-synced with svn, possibly need to declare sync tag?"%(branch,fromver))
                        res.svnrev  = None
                        res.hgver = None
                        return res
                else:
                    ui.status("svn:%s@%s not empty and unsync with hg:%s"%(svn_path, svn_origin.baserev, fromver))
                    res.svnrev  = None
                    res.hgver = None
                    return res
            else:
                ui.status("hg:%s is originated from hgrev %s, wich no synced with svn"%(branch,fromver))

            res.svnrev  = svnrev
            if svnrev:
                ui.status("hgbranch:%s evaluates base svn:%s = hg:%s"%(branch, svnrev, hgrev), level = ui.VERBOSE)
                return res
            if fromver:
                ui.status("hgbranch:%s have unsync parent %s"%(branch, hgrev), level = ui.VERBOSE)
                return res
            ui.status("hgbranch:%s empty - what a ??"%branch, level = ui.VERBOSE)
            res.hgrev = None
            return res
    elif (len(loglines) == 0):
            ui.status("hgbranch:%s at root - what a ??"%branch, level = ui.VERBOSE)
            return res
    ui.status("hgbranch:%s have strange(=multiple) parents"%branch, level = ui.VERBOSE)
    return res

#    get_svn_rev_of_hgbranch returns sync_point with valid svn_base and hgrev, but svnrev=None : this mean that svn have not synced svn_base with hg. 
#       check that this is same point as hgrev and sync them
def check_svn_branch_sync_origin(sync_point, svn_url):
    if not sync_point.svnrev is None:
        return False
    if sync_point.hgrev and sync_point.svn_base:
        #orig_branch = run_hg(["branch"]).strip()
        ui.status("check svn %s@%s is same as hg:%s", svn_url, sync_point.svn_base, sync_point.hgrev);
        svn_switch_to(svn_url, sync_point.svn_base, clean=True, ignore_ancetry=True, propagate_rev=False)
        # Before replicating changes revert directory to previous state...
        run_hg(['revert', '--all', '--no-backup', '-r', sync_point.hgrev])
        # ... and restore .svn directories, if we lost some of them due to removes
        run_svn(['revert', '--recursive', '.'])
        # Do the rest over up-to-date working copy
        # Issue 94 - moved this line to prevent do_svn_copy crashing when its not the first changeset
        run_hg(["up", "-C", sync_point.hgrev])
        if svn_is_clean('.'):
            ui.status("svn branch %s@%s start detected at hg:%s - so mark it",  svn_url, sync_point.svn_base, sync_point.hgrev);
            map_svn_rev_to_hg(sync_point.svn_base, sync_point.hgrev, local=True)
            sync_point.svnrev = sync_point.svn_base
            return True
        ui.status("svn branch %s start is conflicts with hg origin rev:%s", svn_url, sync_point.hgrev, level = ui.VERBOSE)
    return False
    
def get_branch_from_hg(rev_string):
    """
    Given a string identifying an hg revision, get the revision branch.
    """
    args = ["log", "--template", r"{branch}\n", "-r", rev_string]
    return run_hg(args).strip()

def get_branchinfo_from_hg(rev_string):
    """
    Given a string identifying an hg revision, get the revision branch.
    """
    args = ["log", "--template", r"{branch};{tags}\n", "-r", rev_string]
    info = run_hg(args).strip()
    branchname,tags = re.split(";",info)
    tagslist = tags.split()
    return branchname, get_svn_rev_from_tags(tagslist)

def hg_branch_of_work():
    return run_hg(["branch"]).strip()
    
def get_parents_from_hg(rev_string):
    """
    Given a string identifying an hg revision, get the revision branch.
    """
    args = ["parents", "--template", r"{rev}:{node|short}\n", "-r", rev_string]
    lines = run_hg(args).splitlines()
    return [s.strip() for s in lines]

def fixup_hgsvn_dir(basedir='.'):
    """
    Create the hgsvn directory if it does not exist. Useful when using
    repos created by a previous version.
    """
    target = os.path.join(basedir, hgsvn_private_dir)
    if not os.path.exists(target):
        os.mkdir(target)

def get_hgsvn_lock(basedir='.'):
    """
    Get a lock using the hgsvn lock file.
    """
    return _lock(os.path.join(basedir, hgsvn_private_dir, hgsvn_lock_file),
        timeout=0)


def change_to_rootdir():
    """Changes working directory to root of checkout.

    Raises HgSVNError if the current working directory isn't a Mercurial
    repository.
    """
    try:
        root = run_hg(["root"]).strip()
    except ExternalCommandFailed, err:
        raise HgSVNError('No Mercurial repository found.')
    os.chdir(root)


def hg_is_clean(current_branch):
    """Returns False if the local Mercurial repository has
       uncommitted changes."""
    if run_hg(['st', '-mard'], output_is_locale_encoding=True).strip():
        ui.status(("\nThe Mercurial working copy contains pending changes "
                   "in branch '%s'!\n"
                   "Please either commit or discard them before running "
                   "'%s' again."
                   % (current_branch, get_script_name())),
                  level=ui.ERROR)
        return False
    return True


def get_script_name():
    """Helper to return the name of the command line script that was called."""
    return os.path.basename(sys.argv[0])


def hg_force_switch_branch(new_branch, rev_string=None):
    args = ['up', '-C']
    if rev_string is None:
        args.append(new_branch)
    else:
        args.extend(["-r", rev_string])
    run_hg(args)
    run_hg(["branch", new_branch])
    return True


def hg_have_branches():
    hg_branches = [l.split()[0] for l in run_hg(["branches"]).splitlines()]
    return hg_branches

def is_hg_have_branch(branch):
    return (branch in hg_have_branches())

def hg_switch_branch(current_branch, new_branch):
    """Safely switch the Mercurial branch.

    The function will only switch to new_branch iff there are no uncommitted
    changed in the  current branch.

    True is returned if the switch was successful otherwise False.
    """
    if is_hg_have_branch(new_branch):
        # We want to run "hg up -C" (to force changing branches) but we
        # don't want to erase uncommitted changes.
        if not hg_is_clean(current_branch):
            return False
        run_hg(['up', '-C', new_branch])
    else:
        run_hg(["branch", new_branch])
    return True


def check_for_applied_patches():
    """Check for applied mq patches.

    Returns ``True`` if any mq patches are applied, otherwise ``False``.
    """
    try:
        out = run_hg(["qapplied"])
        patches = [s.strip() for s in out.splitlines()]
        if len(patches) > 0:
            return True
    except ExternalCommandFailed, err:
        pass
    return False

def load_hgsvn_branches_map(basedir='.', fname = hgsvn_branchmap_file):
    """
    Get a lock using the hgsvn lock file.
    """
    srcname = os.path.join(basedir, hgsvn_private_dir, fname)
    if os.path.isfile(srcname): # os.path.exists(srcname)
        ui.status("use branch map %s", srcname, level=ui.DEFAULT)
        f = fileinput.FileInput(files=srcname, mode = "r", openhook=fileinput.hook_encoded("utf-8"))
        #f = codecs.open(srcname, "wb", "utf-8")
        #if not f.eof():
        for line in f:
            line = line.strip()
            if(line != "") and (not line.startswith('#')) :
                pair = re.split("=",line)
                if len(pair) == 2:
                    svn_path, hgbranch = pair;
                    hgsvn_branchmap[svn_path] = hgbranch
        f.close()

def save_hgsvn_branches_map(basedir='.', fname = hgsvn_branchmap_file):
    """
    Get a lock using the hgsvn lock file.
    """
    srcname = os.path.join(basedir, hgsvn_private_dir, fname)
    ui.status("save branch map %s", srcname, level=ui.DEFAULT)
    f = codecs.open(srcname, "wb", "utf-8")
    lines = []
    for (svn_path, hgbranch) in hgsvn_branchmap.iteritems():
        lines.append( "%s=%s" % (svn_path, hgbranch) )
    f.write(os.linesep.join(lines))
    f.close()

def is_branchmap_use():
    return (hgsvn_branchmap_options != "")

def is_branchmap_override():
    return ('o' in hgsvn_branchmap_options)

def is_branchmap_append():
    return ('a' in hgsvn_branchmap_options)

def update_config_branchmap(options):
    if options.branchmaping != "":
        global hgsvn_branchmap_options
        hgsvn_branchmap_options = options.branchmaping #re.split(",", options.branchmaping)

def use_branchmap(svn_branch, wc_base):
        if hgsvn_branchmap.has_key(wc_base):
            if hgsvn_branchmap[wc_base] != svn_branch:
              if is_branchmap_override():
                hgsvn_branchmap[wc_base] = svn_branch
                ui.status("override branch map svn:%s  hg:%s" % (wc_base, svn_branch), level=ui.DEFAULT)
        else:
            if is_branchmap_append():
                hgsvn_branchmap[wc_base] = svn_branch
                ui.status("add branch map svn:%s  hg:%s" % (wc_base, svn_branch), level=ui.DEFAULT)

def check_branchmap(svn_branch, wc_base, options):
    global hgsvn_branchmap

    ui.status("branch lookup svn:%s  hg:%s" % (wc_base, svn_branch), level=ui.DEBUG)
    if is_branchmap_use() :
        if hgsvn_branchmap.has_key(wc_base):
            svn_branch = hgsvn_branchmap[wc_base]
            ui.status("use branch map svn:%s  hg:%s" % (wc_base, svn_branch), level=ui.DEFAULT)
        elif svn_branch in hgsvn_branchmap.values():
            svn_branch = "uncknown"

    # if --branch was passed, override the branch name derived above
    if options.svn_branch:
        svn_branch = options.svn_branch
        use_branchmap(svn_branch, wc_base)
    return svn_branch

def svn_base_of_branch(branch):
    for node in hgsvn_branchmap:
        if hgsvn_branchmap[node] == branch:
            return node
    #by default branches maps transparent
    return branch

def svn_branch_of_path(path):
    # get longest branchpath mutching path
    path = os.path.normcase(os.path.normpath(path))
    found = ""
    for node in hgsvn_branchmap:
        if path.startswith(os.path.normcase(os.path.normpath(node))):
            if len(found) < len(node):
                found = node
    if len(found) != 0:
        return found, hgsvn_branchmap[found]
    else:
        return None, None

def load_svnignores(basedir='.', fname = hgsvn_svnignore_file):
    """
    Get svn ignored files list
    """
    srcname = os.path.join(basedir, hgsvn_private_dir, fname)
    if os.path.isfile(srcname): # os.path.exists(srcname)
        ui.status("use svn ignores %s", srcname, level=ui.DEFAULT)
        f = fileinput.FileInput(files=srcname, mode = "r", openhook=fileinput.hook_encoded("utf-8"))
        #f = codecs.open(srcname, "wb", "utf-8")
        #if not f.eof():
        for line in f:
            line = line.strip()
            if(line != "") and (not line.startswith('#')) :
                svn_ignores.append(line)
        f.close()

def save_svnignores(basedir='.', fname = hgsvn_svnignore_file):
    srcname = os.path.join(basedir, hgsvn_private_dir, fname)
    ui.status("save svn ignores to %s", srcname, level=ui.DEFAULT)
    f = codecs.open(srcname, "wb", "utf-8")
    f.write(os.linesep.join(svn_ignores))
    f.close()

def is_ignore4svn(fname):
    return (fname in svn_ignores)

def append_ignore4svn(fname):
    svn_ignores.append(fname)

def hg_subrepos(basedir='.'):
    srcname = os.path.join(basedir, ".hgsub")
    res = list()
    if os.path.isfile(srcname): # os.path.exists(srcname)
        ui.status("use hg subrepos %s", srcname, level=ui.DEFAULT)
        f = fileinput.FileInput(files=srcname, mode = "r", openhook=fileinput.hook_encoded("utf-8"))
        #f = codecs.open(srcname, "wb", "utf-8")
        #if not f.eof():
        for line in f:
            line = line.strip()
            if(line != "") and (not line.startswith('#')) :
                pair = re.split("=",line)
                if len(pair) == 2:
                    wc_path, extern = pair;
                    wc_path = os.path.normcase(os.path.normpath(wc_path))
                    res.append(wc_path)
        f.close()
    return res

def in_pathes(value, pathlist):
    for path in pathlist:
        ui.status("path %s match to %s" %(value, path), level=ui.PARSE)
        if value.startswith(path):
            return True
    return False

# it removes from  paths all pathes that is subdir of some another path in  (paths | ommit_dirs)
def drop_nested_dirs( paths, ommit_dirs=[]):
    ui.status("drop_nested_dirs for %s+%s"%(paths, ommit_dirs), level = ui.PARSE)
    paths = set(paths)
    ommit = set(ommit_dirs)
    paths -= ommit
    alldirs = list(paths | ommit);
    alldirs.sort()
    pred = '.';
    filtered = []
    for p in alldirs:
        if len(pred) >= len(p):
            pred = p
            continue
        L = len(pred)
        separator = p[L]
        ui.status("drop_nested_dirs try:%s #%s"%(p, separator), level = ui.PARSEINNER)
        if not( separator in '/\\'):
            pred = p
            continue
        ui.status("drop_nested_dirs pred:%s <%s> p:%s "%(pred, pred[0:L], p), level = ui.PARSEINNER)
        if p[0:L] != pred[0:L] :
            pred = p
            continue
        paths -= set([p])
        filtered.append(p)
        
    res = list(paths)
    ui.status("drop_nested_dirs have:%s"%res, level = ui.PARSE)
    return res
    

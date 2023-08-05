from hgsvn import ui
from hgsvn.ui import is_debug
from hgsvn.errors import ExternalCommandFailed, HgSVNError, RunCommandError
from hgsvn.shell import (locale_encoding
    , run_args
    )

import os
import hglib

hgseance = None		#hgclient
# this path where seance run from
hgseance_cwd = None

def run_hg(args=None, bulk_args=None, output_is_locale_encoding=False, prompt = None):
    """
    Run a Mercurial command, returns the (unicode) output.
    """
    def invoke_cmd_by_hgseance(args, fail_if_stderr=False):
        global hgseance
        try:
            ui.status("hg %s"%args, level=ui.DEBUG)
            ui.status("hg: %s"%(';'.join(args)), level=ui.DEBUG)
            return hgseance.rawcommand(args, prompt = prompt)
        except (hglib.error.CommandError), e:
            raise RunCommandError("External program failed", e.ret, e.args, e.err, e.out)
    
    enc = locale_encoding; #'utf-8'; #
    
    global hgseance
    global hgseance_cwd

    if not (hgseance is None):
        # if run from other cwd, need reconnect new hg seance to work in current cwd
        if hgseance_cwd != os.getcwd():
            hg_close()

    if hgseance is None:
        hgseance = hglib.open(path='.', encoding=enc)
        enc = hgseance.encoding
        hgseance_cwd = os.getcwd()
    
    try:
        output = run_args(invoke_cmd_by_hgseance, args, bulk_args, enc)
    except :
        #on any exception destroy and recreate new hgseance for next commands
        del hgseance
        hgseance = None
        raise
    
    # some hg cmds, for example "log" return output with mixed encoded lines, therefore decode them 
    # line by line independently
    #outlines = output #.splitlines(True)
    try:
        outlines = unicode(output, encoding='utf-8', errors = 'strict').splitlines(True)
    except:
        binlines = output.splitlines(True);
        outlines = list();
        for line in binlines:
            try:
                #uline = unicode(line, encoding='utf-8', errors = 'ignore')
                uline = line.decode(enc, errors='strict')#encoding or locale_encoding or 'UTF-8'
            except UnicodeDecodeError:
                uline = line.decode(locale_encoding, errors='strict')#encoding or locale_encoding or 'UTF-8'
                if ui._level >= ui.PARSE:
                    print locale_encoding, ":", line
                #uline = unicode(line, encoding=locale_encoding, errors = 'ignore')
            outlines.append(uline)
        
    if ui._level >= ui.PARSE:
        print outlines
    res = ''
    for line in outlines:
        if ui._level >= ui.PARSE:
            print line.encode(locale_encoding)
        res += line
        #try:
        #    res += line.decode(enc, errors='ignore')#encoding or locale_encoding or 'UTF-8'
        #except UnicodeDecodeError:
        #    res += line.decode(locale_encoding, errors='ignore')#encoding or locale_encoding or 'UTF-8'
    return res

def hg_close():
    global hgseance
    if hgseance is None:
        return
    hgseance.close()
    del hgseance
    hgseance = None
    hgseance_cwd = None


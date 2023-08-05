from hgsvn import ui
from hgsvn.ui import is_debug
from hgsvn.errors import ExternalCommandFailed, HgSVNError, RunCommandError

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
import hglib

def c_style_unescape(string):
    if string[0] == string[-1] == '"':
        return string.decode('string-escape')[1:-1]
    return string

# Windows compatibility code by Bill Baxter
if os.name == "nt":
    def find_program(name):
        """
        Find the name of the program for Popen.
        Windows is finnicky about having the complete file name. Popen
        won't search the %PATH% for you automatically.
        (Adapted from ctypes.find_library)
        """
        if os.path.exists(name):
            return name

        # See MSDN for the REAL search order.
        base, ext = os.path.splitext(name)
        if ext:
            exts = [ext]
        else:
            exts = ['.bat', '.exe']
        for directory in os.environ['PATH'].split(os.pathsep):
            if len(directory) <= 1:
                continue
            directory = c_style_unescape(directory)
            for e in exts:
                fname = os.path.join(directory, base + e)
                if os.path.exists(fname):
                    return fname
        return name
else:
    def find_program(name):
        """
        Find the name of the program for Popen.
        On Unix, popen isn't picky about having absolute paths.
        """
        return name


def _rmtree_error_handler(func, path, exc_info):
    """
    Error handler for rmtree. Helps removing the read-only protection under
    Windows (and others?).
    Adapted from http://www.proaxis.com/~darkwing/hot-backup.py
    and http://patchwork.ozlabs.org/bazaar-ng/patch?id=4243
    """
    if func in (os.remove, os.rmdir) and os.path.exists(path):
        # Change from read-only to writeable
        os.chmod(path, os.stat(path).st_mode | stat.S_IWRITE)
        func(path)
    else:
        # something else must be wrong...
        raise

def rmtree(path):
    """
    Wrapper around shutil.rmtree(), to provide more error-resistent behaviour.
    """
    return shutil.rmtree(path, False, _rmtree_error_handler)


locale_encoding = locale.getpreferredencoding()

def get_encoding():
    return locale_encoding

def shell_quote(s):
    if os.name == "nt":
        q = '"'
    else:
        q = "'"
    return q + s.replace('\\', '\\\\').replace("'", "'\"'\"'") + q

def _run_raw_command(cmd, args, fail_if_stderr=False):
    cmd_string = "%s %s" % (cmd,  " ".join(map(shell_quote, args)))
    ui.status("* %s", cmd_string, level=ui.DEBUG)
    try:
        pipe = Popen([cmd] + args, executable=cmd, stdout=PIPE, stderr=PIPE)
    except OSError:
        etype, value = sys.exc_info()[:2]
        raise ExternalCommandFailed(
            "Failed running external program: %s\nError: %s"
            % (cmd_string, "".join(traceback.format_exception_only(etype, value))))
    out, err = pipe.communicate()
    if "nothing changed" == out.strip(): # skip this error
        return out
    if pipe.returncode != 0 or (fail_if_stderr and err.strip()):
        raise RunCommandError("External program failed", pipe.returncode, cmd_string, err, out)
    return out

def getstatusoutput(cmd): 
    """Return (status, output) of executing cmd in a shell."""
    """This new implementation should work on all platforms."""
    import subprocess
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)  
    output = "".join(pipe.stdout.readlines()) 
    sts = pipe.returncode
    if sts is None: sts = 0
    return sts, output
    
def _run_raw_shell_command(cmd):
    ui.status("* %s", cmd, level=ui.DEBUG)
    st, out = getstatusoutput(cmd)
    if st != 0:
        raise RunCommandError("External program failed with non-zero return code", st, cmd, "", out)
    return out

def run_args(cmd, args=None, bulk_args=None, encoding=None, fail_if_stderr=False):
    """
    Run a command without using the shell.
    """
    args = args or []
    bulk_args = bulk_args or []

    def _transform_arg(a):
        #assumes that args passes as utf8
        if isinstance(a, unicode):
            a = str(a.encode(encoding or locale_encoding or 'UTF-8'))
            ui.status("take param %s as encode %s"%(a, encoding), level=ui.TRACECMD)
        elif not isinstance(a, str):
            a = str(a)
            ui.status("take str %s as encode %s"%(a, encoding), level=ui.TRACECMD)
        #a = a.encode(encoding or locale_encoding or 'UTF-8');
        return a

    safeargs = []
    for a in args: 
        safeargs.append(_transform_arg(a))

    if not bulk_args:
        return cmd(safeargs, fail_if_stderr)
    # If one of bulk_args starts with a slash (e.g. '-foo.php'),
    # hg and svn will take this as an option. Adding '--' ends the search for
    # further options.
    for a in bulk_args:
        if a.strip().startswith('-'):
            args.append("--")
            break
    max_args_num = 254
    i = 0
    out = ""
    while i < len(bulk_args):
        stop = i + max_args_num - len(args)
        sub_args = []
        for a in bulk_args[i:stop]:
            sub_args.append(_transform_arg(a))
        out += cmd(safeargs + sub_args, fail_if_stderr)
        i = stop
    return out

def run_command(cmd, args=None, bulk_args=None, encoding=None, fail_if_stderr=False):
    cmd = find_program(cmd)

    def invoke_cmd_by_raw(args, fail_if_stderr=False):
        return _run_raw_command(cmd, args, fail_if_stderr)

    return run_args(invoke_cmd_by_raw, args, bulk_args, encoding, fail_if_stderr)

def run_shell_command(cmd, args=None, bulk_args=None, encoding=None):
    """
    Run a shell command, properly quoting and encoding arguments.
    Probably only works on Un*x-like systems.
    """
    def invoke_cmd_by_shell(args, fail_if_stderr=False):
        def _quote_arg(a):
            return shell_quote(a)
        
        shell_cmd = cmd
        if args:
            shell_cmd += " " + " ".join(a for a in args)
        
        return _run_raw_shell_command(shell_cmd)
    
    return run_args(invoke_cmd_by_shell, args, bulk_args, encoding)

def once_or_more(desc, retry, function, *args, **kwargs):
    """Try executing the provided function at least once.

    If ``retry`` is ``True``, running the function with the given arguments
    if an ``Exception`` is raised. Otherwise, only run the function once.

    The string ``desc`` should be set to a short description of the operation.
    """
    while True:
        try:
            return function(*args, **kwargs)
        except Exception, e:
            ui.status('%s failed: %s', desc, str(e))
            if retry:
                ui.status('Trying %s again...', desc)
                continue
            else:
                raise

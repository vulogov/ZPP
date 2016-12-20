##
##
##
import os

def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring

def check_file(fname, mode):
    fname = os.path.expandvars(fname)
    if os.path.exists(fname) and os.path.isfile(fname) and os.access(fname, mode):
        return True
    return False

def check_directory(dname):
    dname = os.path.expandvars(dname)
    if os.path.exists(dname) and os.path.isdir(dname) and os.access(dname, os.R_OK):
        return True
    return False

def check_directory_write(dname):
    dname = os.path.expandvars(dname)
    if os.path.exists(dname) and os.path.isdir(dname) and os.access(dname, os.W_OK):
        return True
    return False


def check_file_read(fname):
    return check_file(fname, os.R_OK)

def check_module(fname):
    if not check_file_read(fname):
        return False
    if os.path.getsize(fname) > 0:
        return True
    return False

def check_file_write(fname):
    return check_file(fname, os.W_OK)

def check_file_exec(fname):
    return check_file(fname, os.X_OK)

def get_dir_content(dname):
    if not check_directory(dname):
        return []
    ret = []
    for f in os.listdir(dname):
        if not check_file_read("%s/%s"%(dname, f)):
            continue
        ret.append((f, "%s/%s"%(dname, f), os.path.splitext(f)))
    return ret

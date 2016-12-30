__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import clips

check_file_read_clips="(deffunction check_file_read (?str ) (python-call _check_file_read ?str ))"
check_file_write_clips="(deffunction check_file_write (?str ) (python-call _check_file_write ?str ))"
check_directory_clips="(deffunction check_directory (?str ) (python-call _check_directory ?str ))"


def _check_file_read(_str):
    from zpp_lib import check_file_read
    if check_file_read(str(_str)) == True:
        return clips.Symbol('TRUE')
    return clips.Symbol('FALSE')

def _check_file_write(_str):
    from zpp_lib import check_file_write
    if check_file_wrie(str(_str)) == True:
        return clips.Symbol('TRUE')
    return clips.Symbol('FALSE')

def _check_directory(_str):
    from zpp_lib import check_directory
    if check_directory(str(_str)) == True:
        return clips.Symbol('TRUE')
    return clips.Symbol('FALSE')
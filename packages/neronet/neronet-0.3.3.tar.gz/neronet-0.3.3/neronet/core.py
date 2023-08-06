# -*- coding: utf-8 -*-
# core.py
#
# Core class and function definitions

import os
import sys
import datetime
import subprocess
import shlex
import importlib
import traceback

TIME_OUT = 5.0
"""float: how long the socket waits before failing when sending data
"""
NERONET_DIR_NAME = '.neronet'
USER_DATA_DIR = '~/' + NERONET_DIR_NAME # Remember to os.path.expanduser
USER_DATA_DIR_ABS = os.path.expanduser(USER_DATA_DIR)

class Runresult: """A class for holding shell command execution results."""

def remove_data():
    """Removes the neronet data files
    """
    if os.path.exists(USER_DATA_DIR_ABS):
        os.system('rm -r ' + USER_DATA_DIR_ABS)

def osrunroe(cmd, verbose=False, inp=None):
    """Execute a shell command and return the return code, stdout and -err.

    Args:
        verbose (boolean): Whether to print command or not.
        inp (str): Input string for the sub process.

    Returns
        Runresult: The result object of the executed command.
    """
    if verbose: print('> %s' % (cmd))
    if type(cmd) == str:
        cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    res = Runresult()
    res.cmd = cmd
    res.out, res.err = proc.communicate(inp)
    res.rv = proc.poll()
    return res

def osrun(cmd):
    res = osrunroe(cmd)
    if res.rv != 0:
        raise RuntimeError('osrun(%s) failed! Err: "%s", Out: "%s".' \
                % (res.cmd, res.err, res.out))
    return res


def get_hostname():
    return osrun('hostname').out.strip()

def time_now():
    return datetime.datetime.now() #.strftime('%H:%M:%S %d-%m-%Y')

def write_file(filepath, data):
    text = str(data)
    with open(filepath, 'w') as f:
        f.write(text)

def read_file(filepath, default=None):
    result = default
    try:
        with open(filepath, 'r') as f:
            result = ''
            for line in f:
                result += line
    except IOError as e:
        pass
    return result

#Warning copies the whole construct so might take a lot of memory if the
#original construct was large
def lod_to_dol(self, lod):
    """Convert a list of dicts to a dict of lists
    """
    dol = {}
    for dict_item in lod:
        for key, value in dict_item.items():
            if key not in dol:
                key[dol] = [value]
            else:
                key[dol].appen(value)
    return dol

#IMPORTANT: This function shouldn't be used if the module cannot be imported
def import_from(module_name, obj_name):
    """Import object from module, tries to first find module from
    neronet/scripts

    Parameters:
        module (str): name of the module to be imported from
        obj_name (str): name of the object to be imported

    Returns:
        object: The object to be imported
    
    Raises:
        ImportError: If the module to be imported couldn't be imported
    """
    #FIXME: Remove dependancy for neronet.scripts.
    try:
        module = importlib.import_module("neronet.scripts." + module_name)
        obj = getattr(module, obj_name)
        return obj
    except:
        raise ImportError("Something went wrong while trying to "
                        "import %s from %s:\n" % (obj_name, module_name) + \
                            traceback.format_exc())

def can_import(module_name, obj_name):
    """Checks if object can be imported from module or if the module exists

    Parameters:
        module (str): name of the module to be imported from
        obj_name (str): name of the object to be imported

    Returns:
        boolean: True if the object can be imported
    """
    #FIXME: Remove dependancy for neronet.scripts.
    try:
        module = importlib.import_module("neronet.scripts." + module_name)
        obj = getattr(module, obj_name)
    except:
        return False
    return True

def create_config_template(expid='exp_id', runcmdprefix='python', maincodefile='main.py', *params):
    # Creates a config file with the required fields.
    if os.path.exists('config.yaml'):
        print('A config.yaml file already exists in this folder.')
        return
    with open('config.yaml', 'w') as f:
        f.write('+%s:\n' % expid)
        f.write('    run_command_prefix: %s\n' % runcmdprefix)
        f.write('    main_code_file: %s\n' % maincodefile)
        f.write('    parameters:\n')
        if params:
            params_format = ''
            for param in params:
                f.write('        %s:\n' % param)
                params_format += '{%s} ' % param
            f.write("    parameters_format: '%s'\n" % params_format) 
        else:
            f.write('    parameters_format:\n')
        

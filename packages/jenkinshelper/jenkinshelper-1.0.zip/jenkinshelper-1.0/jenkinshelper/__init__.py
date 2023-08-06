"""Useful tools for continuous integration"""

import os
import subprocess
import shutil
import time
from jenkinshelper import log

ROOT_WORKING_DIR = os.getcwd()

class PushDir(object):
    """Context Manager for changing the cwd"""
    def __init__(self, new_dir):
        self.old_dir = os.getcwd()
        self.new_dir = new_dir
    def __enter__(self):
        os.chdir(self.new_dir)
    def __exit__(self, _type, value, traceback):
        os.chdir(self.old_dir)

def run(cmd, may_fail=False):
    """Runs a cmd and prints it first"""
    path = os.path.relpath(os.getcwd(), ROOT_WORKING_DIR)
    if path == ".":
        path = ""
    else:
        path += " "
    print("\x1b[1;34m{}$ {}\x1b[0m".format(path, cmd))
    if may_fail:
        subprocess.call(cmd, shell=True)
    else:
        subprocess.check_call(cmd, shell=True)

def load_env(cmd):
    """Runs a cmd and loads the environment variables it sets"""
    log.info("Loading environment variables from " + cmd)
    variables = subprocess.check_output(cmd + ' && set')
    for var in variables.splitlines():
        var = var.decode('cp1252') # FIXME: This works on (German?) Windows only
        k, _, val = [x.strip() for x in var.strip().partition('=')]
        if k.startswith('?') or k == '':
            continue
        os.environ[k] = val

def rmdir(directory):
    """Removes a directory with multiple tries. On Windows this is needed, because read access by a
    random program causes a remove operation to fail."""
    log.info("Removing directory " + directory)
    tries = 0
    try:
        shutil.rmtree(directory)
    except PermissionError as err:
        tries += 1
        if tries > 100:
            raise err
        else:
            time.sleep(0.1)

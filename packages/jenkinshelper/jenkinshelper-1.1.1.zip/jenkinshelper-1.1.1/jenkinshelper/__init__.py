"""Useful tools for continuous integration"""

import os
import subprocess
import shutil
import time
import sys
import psutil
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

def run(cmd, may_fail=False, max_output_lines=-1):
    """Runs a cmd and prints it first"""
    path = os.path.relpath(os.getcwd(), ROOT_WORKING_DIR)
    if path == ".":
        path = ""
    else:
        path += " "
    print("\x1b[1;34m{}$ {}\x1b[0m".format(path, cmd))
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    printed_lines = 0
    while True:
        line = proc.stdout.readline()
        if line != b'':
            if max_output_lines >= 0 and printed_lines >= max_output_lines:
                log.error("Command output exceeds {} line{}.".format(
                    max_output_lines, "" if max_output_lines == 1 else "s"
                ))
                process = psutil.Process(proc.pid)
                for child in process.children(recursive=True):
                    child.kill()
                proc.kill()
                break
            sys.stdout.buffer.write(line)
            printed_lines += 1
        else:
            break
    proc.wait()
    if not may_fail and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)

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
    while True:
        try:
            shutil.rmtree(directory)
            return
        except PermissionError as err:
            tries += 1
            if tries > 100:
                raise err
            else:
                time.sleep(0.01)

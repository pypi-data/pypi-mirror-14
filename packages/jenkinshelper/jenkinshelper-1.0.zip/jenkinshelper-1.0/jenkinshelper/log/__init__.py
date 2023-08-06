"""Print colored messages"""

def info(text):
    """Print a blue message"""
    print("\x1b[1;34m{}\x1b[0m".format(text))

def error(text):
    """Print a red message"""
    print("\x1b[1;31m{}\x1b[0m".format(text))

def warn(text):
    """Print a yellow message"""
    print("\x1b[1;33m{}\x1b[0m".format(text))

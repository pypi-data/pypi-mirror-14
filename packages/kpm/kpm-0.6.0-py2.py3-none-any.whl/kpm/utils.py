import errno
import os
from termcolor import colored


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def color_bool(status):
    if status:
        return colored('ok', 'green')
    else:
        return colored('changed', 'yellow')

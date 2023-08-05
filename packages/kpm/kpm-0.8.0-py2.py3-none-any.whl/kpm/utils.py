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


def color_bool(status, msg=[("ok", 'green'), ("changed", 'yellow')]):
    if status is True:
        return colored(msg[0][0], msg[0][1])
    elif status is False:
        return colored(msg[1][0], msg[1][1])

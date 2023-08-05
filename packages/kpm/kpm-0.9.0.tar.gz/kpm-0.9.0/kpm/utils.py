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


def colorize(status, msg={True: {'msg': 'ok', 'color': 'green'},
                          False: {'msg': 'changed', 'color': 'yellow'}}):
    return colored(msg[status]['msg'], msg[status]['color'])

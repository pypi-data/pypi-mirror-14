import os.path
from kpm.utils import mkdir_p


def get_token():
    path = ".kpm/auth_token"
    home = os.path.expanduser("~")
    tokenfile = os.path.join(home, path)
    if os.path.exists(tokenfile):
        f = open(tokenfile, 'r')
        token = f.read()
        f.close()
        return token
    else:
        return None


def set_token(token):
    path = ".kpm/auth_token"
    home = os.path.expanduser("~")
    tokenfile = os.path.join(home, path)
    mkdir_p(os.path.join(home, ".kpm"))
    f = open(tokenfile, 'w')
    f.write(token)
    f.close()

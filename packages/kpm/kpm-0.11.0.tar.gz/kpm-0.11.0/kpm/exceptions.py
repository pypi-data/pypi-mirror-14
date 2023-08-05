from __future__ import absolute_import


class KpmHubBadPassword(Exception):
    """Issue with login to kpm hub"""
    def __init__(self):
        super(KpmHubBadPassword, self).__init__()

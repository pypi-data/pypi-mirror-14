import json
import logging
from urlparse import urlparse
from urlparse import urljoin
import requests

__all__ = ['Registry']

logger = logging.getLogger(__name__)
DEFAULT_REGISTRY = "https://kpm-api.kubespray.io"


class Registry(object):
    def __init__(self, endpoint=DEFAULT_REGISTRY):
        if endpoint is None:
            endpoint = DEFAULT_REGISTRY
        self.endpoint = urlparse(endpoint)
        self.headers = {'Content-Type': 'application/json'}

    def _url(self, path):
        return urljoin(self.endpoint.geturl(), path)

    def pull(self, name, version=None):
        path = "/packages/install.json"
        params = {"name": name}
        if version:
            params['version'] = version
        r = requests.get(self._url(path), params=params, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def push(self, body, force=False):
        path = "/packages.json"
        r = requests.post(self._url(path),
                          params={"force": str(force).lower()},
                          data=json.dumps(body), headers=self.headers)
        r.raise_for_status()
        return r.json()

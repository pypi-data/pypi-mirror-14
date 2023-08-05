import time
import logging
import json
import yaml
import subprocess
import tempfile


__all__ = ['Kubernetes', "get_endpoint"]


logger = logging.getLogger(__name__)


resource_endpoints = {
    "daemonsets": "/api/v1/namespaces/{namespace}/daemonsets",
    "deployments": "/api/v1/namespaces/{namespace}/deployments",
    "horizontalpodautoscalers": "/api/v1/namespaces/{namespace}/horizontalpodautoscalers",
    "ingresses": "/api/v1/namespaces/{namespace}/ingresses",
    "jobs": "/api/v1/namespaces/{namespace}/jobs",
    "namespaces": "/api/v1/namespaces",
    "persistentvolumes": "/api/v1/namespaces/{namespace}/persistentvolumes",
    "persistentvolumeclaims": "/api/v1/namespaces/{namespace}/persistentvolumeclaims",
    "services": "/api/v1/namespaces/{namespace}/services",
    "serviceaccounts": "/api/v1/namespaces/{namespace}/serviceaccounts",
    "replicationcontrollers": "/api/v1/namespaces/{namespace}/replicationcontrollers",
}


resources_alias = {"ds": "daemonsets",
                   "hpa": "horizontalpodautoscalers",
                   "ing": "ingresses",
                   "ns": "namespaces",
                   "po": "pods",
                   "pv": "persistentvolumes",
                   "pvc": "persistentvolumeclaims",
                   "rc": "replicationcontrollers",
                   "svc": "services"}


def get_endpoint(kind):
    name = None
    if kind in resource_endpoints:
        name = kind
    elif kind in resources_alias:
        name = resources_alias[kind]
    elif kind + "s" in resource_endpoints:
        name = kind + "s"
    else:
        raise StandardError("Resource name %s not in [%s]" % (kind, resource_endpoints.keys()))
    return resource_endpoints[name]


class Kubernetes(object):
    def __init__(self, resource, namespace=None):
        self.filepath = resource
        self.obj = None
        self.protected = False
        self._resource_load(self.filepath)
        self.kind = self.obj['kind'].lower()
        self.name = self.obj['metadata']['name']
        self.version = self._get_version(self.obj)
        self.namespace = self._namespace(namespace)
        self.result = None

    def _resource_load(self, resourcepath):
        f = open(resourcepath, 'r')
        self.obj = yaml.load(f)
        f.close()
        if 'annotations' in self.obj['metadata']:
            if ('kpm.protected' in self.obj['metadata']['annotations']
                and self.obj['metadata']['annotations']['kpm.protected'] == 'true'):
                self.protected = True

    def _namespace(self, namespace=None):
        if namespace:
            return namespace
        elif 'namespace' in self.obj['metadata']:
            return self.obj['metadata']['namespace']
        else:
            return 'default'

    def create(self, force=False, namespace=None, dry=False):
        """
          - Check if resource name exists
          - if it exists check if the version is the same
          - if not the same delete the resource and recreate it
          - if force == true, delete the resource and recreate it
          - if doesnt exists create it
        """
        if namespace:
            self.namespace = self._namespace(namespace)

        r = self.get()
        cmd = ['create', '-f', self.filepath]
        if r is None:
            if not dry:
                self._call(cmd)
            return False
        elif (self.version is None or self._get_version(r) == self.version) and force is False:
            return True
        elif self._get_version(r) != self.version or force is True:
            if not dry:
                self.delete()
                self._call(cmd)
            return False

    def _get_version(self, r):
        if 'annotations' in r['metadata'] and 'kpm.hash' in r['metadata']['annotations']:
            return r['metadata']['annotations']['kpm.hash']
        else:
            return None

    def get(self):
        cmd = ['get', self.kind, self.name, '-o', 'json']
        try:
            self.result = json.loads(self._call(cmd))
            return self.result
        except subprocess.CalledProcessError:
            return None

    def delete(self, namespace=None, check=False, dry=False):
        cmd = ['delete', self.kind, self.name]
        if self.protected:
            return True
        if check is False:
            self._call(cmd)
            return False
        else:
            if namespace:
                self.namespace = self._namespace(namespace)
            r = self.get()
            if r is not None:
                if not dry:
                    self._call(cmd)
                return False
            else:
                return True

    def wait(self, retries=3, seconds=1):
        r = 0
        while (r < retries and self.get() is None):
            time.sleep(seconds)

    def exists(self):
        r = self.get()
        if r is None:
            return False
        else:
            return True

    def _call(self, cmd):
        command = ['kubectl'] + cmd + ["--namespace", self.namespace]
        return subprocess.check_output(command, stderr=subprocess.STDOUT)

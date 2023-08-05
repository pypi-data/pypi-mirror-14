import io
import logging
import json
import yaml
import subprocess
import tempfile
import tarfile
from tabulate import tabulate

__all__ = ['Kubernetes']


logger = logging.getLogger(__name__)


class Kubernetes(object):
    def __init__(self, resource, namespace=None):
        self.filepath = resource
        self.obj = None
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

    def _namespace(self, namespace=None):
        if namespace:
            return namespace
        elif 'namespace' in self.obj['metadata']:
            return self.obj['metadata']['namespace']
        else:
            return 'default'

    def create_namespace(self, namespace, dry=False):
        value = """
        apiVersion: v1
        kind: Namespace
        metadata:
          name: {namespace}
        """.format(namespace=namespace)
        f = tempfile.NamedTemporaryFile()
        f.write(value)
        f.flush()
        resource = Kubernetes(f.name)
        r = resource.create(create_ns=False, dry=dry)
        f.close()
        return r

    def create(self, force=False, namespace=None, dry=False, create_ns=True):
        """
          - Check if resource name exists
          - if it exists check if the version is the same
          - if not the same delete the resource and recreate it
          - if force == true, delete the resource and recreate it
          - if doesnt exists create it
        """
        if namespace:
            self.namespace = self._namespace(namespace)
        if create_ns:
            self.create_namespace(self.namespace, dry=dry)

        r = self.get()
        cmd = ['create', '-f', self.filepath]
        if r is None:
            if not dry:
                self._call(cmd)
            return False
        elif self._get_version(r) == self.version and force is False:
            return True
        elif self._get_version(r) != self.version or force is True:
            if not dry:
                self.delete()
                self._call(cmd)
            return False

    def _get_version(self, r):
        if 'labels' in r['metadata'] and 'kpm.version' in r['metadata']['labels']:
            return r['metadata']['labels']['kpm.version']
        else:
            return None

    def get(self):
        cmd = ['get', self.kind, self.name, '-o', 'json']
        try:
            self.result = json.loads(self._call(cmd))
            return self.result
        except subprocess.CalledProcessError:
            return None

    def delete(self):
        cmd = ['delete', self.kind, self.name]
        return self._call(cmd)

    def exists(self):
        r = self.get()
        if r is None:
            return False
        else:
            return True

    def _call(self, cmd):
        command = ['kubectl'] + cmd + ["--namespace", self.namespace]
        return subprocess.check_output(command, stderr=subprocess.STDOUT)

import io
import logging
import tarfile
import os.path
from tabulate import tabulate

from kpm.kubernetes import Kubernetes
from kpm.registry import Registry
from kpm.utils import mkdir_p, color_bool

__all__ = ['Kubernetes']


logger = logging.getLogger(__name__)


def install(package_name,
            version=None,
            dest="/tmp",
            namespace=None,
            force=False,
            dry=False,
            endpoint=None):
    registry = Registry(endpoint=endpoint)
    io_tar = io.BytesIO(registry.install(package_name, namespace=namespace, version=version).encode())
    tar = tarfile.open(fileobj=io_tar, mode='r')
    package_dir = os.path.join(dest, tar.getmembers()[0].name)
    mkdir_p(dest)
    tar.extractall(dest)
    table = []
    for resource in sorted(os.listdir(package_dir)):
        filepath = os.path.join(package_dir, resource)
        kubresource = Kubernetes(filepath, namespace)
        status = kubresource.create(namespace=namespace, force=force, dry=dry)
        order, organization, name, version, _ = resource.split(":")
        table.append(["%02d" % int(order), "%s/%s=%s" % (organization, name, version),
                      kubresource.kind, kubresource.name, kubresource.namespace, color_bool(status)])
    print_result(package_name, table)


def print_result(name, table):
    headers = ["order", "app", "type", "name",  "namespace", "status"]
    print "Deploy: %s" % name
    print tabulate(table, headers, tablefmt="fancy_grid")

import re
import io
import logging
import tarfile
import os.path
import glob

from kpm.kubernetes import Kubernetes
from kpm.registry import Registry
from kpm.utils import color_bool
from kpm.display import print_deploy_result

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
    tar.extractall(dest)
    table = []
    files = []

    for info in tar.getmembers():
        if re.match(".*\.ya?ml", info.name) is not None:
            files.append(os.path.join(dest, info.name))

    for resource in sorted(files):
        kubresource = Kubernetes(resource, namespace)
        status = kubresource.create(namespace=namespace, force=force, dry=dry)
        _, organization, name, version, _ = os.path.basename(resource).split(":")
        table.append(["%s/%s" % (organization, name), version,
                      kubresource.kind, kubresource.name, kubresource.namespace, color_bool(status)])
    print_deploy_result(package_name, table)


def delete(package_name,
           version=None,
           dest="/tmp",
           namespace=None,
           dry=False,
           endpoint=None):
    registry = Registry(endpoint=endpoint)
    io_tar = io.BytesIO(registry.install(package_name, namespace=namespace, version=version).encode())
    tar = tarfile.open(fileobj=io_tar, mode='r')
    tar.extractall(dest)
    table = []
    files = []

    for info in tar.getmembers():
        if re.match(".*\.ya?ml", info.name) is not None:
            files.append(os.path.join(dest, info.name))

    for resource in sorted(files):
        kubresource = Kubernetes(resource, namespace)
        status = kubresource.delete(namespace=namespace, check=True, dry=dry)
        _, organization, name, version, _ = os.path.basename(resource).split(":")
        # "%02d" % int(order),
        table.append(["%s/%s" % (organization, name), version,
                      kubresource.kind, kubresource.name,
                      kubresource.namespace,
                      color_bool(status, msg=[("absent", "green"), ("deleted", "yellow")])])
    print_deploy_result(package_name, table)

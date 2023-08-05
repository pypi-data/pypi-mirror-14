import logging

import os.path
from kpm.kubernetes import Kubernetes
from kpm.registry import Registry
from kpm.utils import colorize, mkdir_p
from kpm.display import print_deploy_result

logger = logging.getLogger(__name__)


def deploy(package_name,
           version=None,
           dest="/tmp",
           namespace=None,
           force=False,
           dry=False,
           endpoint=None):

    registry = Registry(endpoint=endpoint)
    packages = registry.generate(package_name, namespace=namespace, version=version)
    dest = os.path.join(dest, package_name)
    if version:
        dest = os.path.join(dest, version)
    mkdir_p(dest)
    table = []
    print "Deploying %s" % package_name
    i = 0
    for package in packages["deploy"]:
        i += 1
        organization, name = package["package"].split("/")
        version = package["version"]
        namespace = package["namespace"]
        print "\n %02d - %s:" % (i, package["package"])
        for resource in package["resources"]:
            body = resource["body"]
            endpoint = resource["endpoint"]
            # Use API instead of kubectl
            f = open(os.path.join(dest, resource['file']), 'wb')
            f.write(body)
            f.flush()
            f.close()
            kubresource = Kubernetes(f.name, namespace)
            status = kubresource.create(namespace=namespace, force=force, dry=dry)
            print " --> %s (%s): %s" % (kubresource.name, kubresource.kind, colorize(status))
            result_line = ["%s/%s" % (organization, name), version,
                           kubresource.kind, kubresource.name,
                           kubresource.namespace, colorize(status)]
            kubresource.wait(5)
            table.append(result_line)

    print_deploy_result(package_name, table)


# @TODO: Delete/deploy are the same!!!
def delete(package_name,
           version=None,
           dest="/tmp",
           namespace=None,
           force=False,
           dry=False,
           endpoint=None):

    registry = Registry(endpoint=endpoint)
    packages = registry.generate(package_name, namespace=namespace, version=version)
    dest = os.path.join(dest, package_name)
    if version:
        dest = os.path.join(dest, version)
    mkdir_p(dest)
    table = []
    print "Removing %s" % package_name
    i = 0
    status_color = {True: {'msg': 'absent', 'color': 'green'},
                    False: {'msg': 'deleted', 'color': 'yellow'},
                    "protected": {'msg': 'protected', 'color': 'blue'}}
    for package in packages["deploy"]:
        i += 1
        organization, name = package["package"].split("/")
        version = package["version"]
        namespace = package["namespace"]
        print "\n %02d - %s:" % (i, package["package"])
        for resource in package["resources"]:
            body = resource["body"]
            endpoint = resource["endpoint"]
            # Use API instead of kubectl
            f = open(os.path.join(dest, resource['file']), 'wb')
            f.write(body)
            f.flush()
            f.close()
            kubresource = Kubernetes(f.name, namespace)
            status = kubresource.delete(namespace=namespace, dry=dry)
            if kubresource.protected:
                status = 'protected'
            print " --> %s (%s): %s" % (kubresource.name, kubresource.kind, colorize(status, msg=status_color))
            result_line = ["%s/%s" % (organization, name), version,
                           kubresource.kind, kubresource.name,
                           kubresource.namespace, colorize(status, msg=status_color)]
            table.append(result_line)

    print_deploy_result(package_name, table)

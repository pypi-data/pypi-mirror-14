import logging
from tabulate import tabulate


logger = logging.getLogger(__name__)


def print_packages(packages):
    header = ['app', 'version', 'privacy', 'downloads']
    table = []

    def _strprivate(val):
        if val:
            return "private"
        else:
            return "public"
    for p in packages:
        table.append([p['name'], p['version'], _strprivate(p['private']), str(p['downloads'])])
    print tabulate(table, header)


def print_deploy_result(table):
    header = ["app", "version", "type", "name",  "namespace", "status"]
    print "\n"
    print tabulate(table, header)

import os

from email.parser import Parser

PKG_INFO_FILENAME = 'PKG-INFO'
SOURCES_FILENAME = 'SOURCES.txt'


def get_egg_info(path):
    for item in os.listdir(path):
        if item.endswith('.egg-info'):
            yield os.path.join(path, item)


def get_sources(path):
    with open(os.path.join(path, SOURCES_FILENAME), 'rb') as fh:
        return fh.read().strip().splitlines()


def find_package():
    sep = os.path.sep
    source_path = __file__[__file__.find(sep, 1)+1:]

    dirname = os.path.dirname(__file__)
    if dirname == '':
        dirname = os.getcwd()

    dirname = os.path.abspath(dirname)

    while dirname != '/':
        for item in get_egg_info(dirname):
            if source_path in get_sources(item):
                return item

        dirname = os.path.dirname(dirname)


def get_version():
    package = find_package()
    if package is None:
        return 'dev'

    pkg_info_path = os.path.join(package, PKG_INFO_FILENAME)

    with open(pkg_info_path, 'rb') as fh:
        parsed = Parser().parse(fh)

    return parsed.get('Version')

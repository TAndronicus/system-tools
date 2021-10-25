import re
from os import listdir
from utils import get_latest_version, remove_unless_dry_run

import Constants


def check_and_clean(path):
    clean_meta(path)
    for ide_catalog in Constants.IDE_CATALOGS:
        print('Cleaning binaries for ' + ide_catalog)
        clean_binaries_and_plugins('/'.join([path, Constants.TOOLBOX_CATALOG, ide_catalog, Constants.INNER_CATALOG]))


def clean_binaries_and_plugins(path):
    versioned_files = list(filter(
        lambda file_name: re.match(Constants.VERSION_REGEX, file_name),
        listdir(path)
    ))
    versions = list(map(
        lambda file_name: re.search(Constants.VERSION_REGEX, file_name).group(0),
        versioned_files
    ))
    latest_version = get_latest_version(versions)
    for file_name in versioned_files:
        if latest_version not in file_name:
            remove_unless_dry_run(path, file_name)


def clean_meta(path):
    files = listdir(path)
    for prefix in Constants.IDE_PREFIXES:
        clean_meta_for_ide(path, files, prefix)


def clean_meta_for_ide(path, files, prefix):
    print('Cleaning meta for ' + prefix)
    ide_versions = to_versions_map(files, prefix)
    latest_version = get_latest_version(ide_versions.keys())
    for current_version, current_name in ide_versions.items():
        if current_version != latest_version:
            remove_unless_dry_run(path, current_name)


def to_versions_map(files, prefix):
    ide_versions = {}
    ide_directories = filter(lambda name: name.startswith(prefix), files)
    for ide_directory_name in ide_directories:
        ide_versions[ide_directory_name.split(prefix)[1]] = ide_directory_name
    return ide_versions


if __name__ == '__main__':
    check_and_clean(Constants.JETBRAINS_PATH)

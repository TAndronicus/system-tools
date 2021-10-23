from os.path import isdir
from os import listdir
import shutil
import semver

import Constants

# Change to True to get a log of what will be removed
dry_run = False


def check_and_clean(path):
    files = listdir(path)
    if contains_only_files(files, path):
        return
    directories = filter_out_nones(files)
    latest_version = get_latest_version(directories)
    if latest_version is None:
        clean_recursively(path, directories)
    elif len(directories) == 1:
        return
    else:
        print('Update ' + path.split(Constants.M2_PATH)[1])
        for directory_name in directories:
            if directory_name == latest_version:
                continue
            print(directory_name + ' (Has newer version: ' + latest_version + ')')
            remove_unless_dry_run(path, directory_name)


def contains_only_files(files, path):
    only_files = True
    for index, file in enumerate(files):
        if isdir('/'.join([path, file])):
            only_files = False
        else:
            files[index] = None
    return only_files


def filter_out_nones(files):
    return [d for d in files if d is not None]


def get_latest_version(directories):
    if len(directories) == 0:
        return None
    latest_version = directories[0]
    for current_directory_name in directories:
        try:
            current_version = semver.VersionInfo.parse(current_directory_name)
            if current_version.compare(latest_version) > 0:
                latest_version = current_directory_name
        except ValueError:
            print('Could not parse version: ' + current_directory_name + '')
            return None
    return latest_version


def clean_recursively(path, directories):
    for directory in directories:
        check_and_clean('/'.join([path, directory]))


def remove_unless_dry_run(path, directory_name):
    if not dry_run:
        shutil.rmtree('/'.join([path, directory_name]))


if __name__ == '__main__':
    check_and_clean(Constants.M2_PATH)

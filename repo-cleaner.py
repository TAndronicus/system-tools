from os.path import isdir
from os import listdir
import shutil
import semver

import Constants

# Change to True to get a log of what will be removed
dry_run = False


def check_and_clean(path):
    files = listdir(path)
    only_files = True
    for index, file in enumerate(files):
        if isdir('/'.join([path, file])):
            only_files = False
        else:
            files[index] = None
    if only_files:
        return

    directories = [d for d in files if d is not None]
    latest_version = check_if_versions(directories)
    if latest_version is None:
        for directory in directories:
            check_and_clean('/'.join([path, directory]))
    elif len(directories) == 1:
        return
    else:
        print('Update ' + path.split(Constants.m2_path)[1])
        for directory in directories:
            if directory == latest_version:
                continue
            print(directory + ' (Has newer version: ' + latest_version + ')')
            if not dry_run:
                shutil.rmtree('/'.join([path, directory]))


def check_if_versions(directories):
    if len(directories) == 0:
        return None
    latest_version = ''
    for directory in directories:
        try:
            current_version = semver.VersionInfo.parse(directory)
        except ValueError:
            return None
        if latest_version == '':
            latest_version = directory
        if current_version.compare(latest_version) > 0:
            latest_version = directory
    return latest_version


if __name__ == '__main__':
    check_and_clean(Constants.m2_path)

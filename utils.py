import semver
import re
import shutil
from Constants import VERSION_REGEX
from Config import use_semver, dry_run


def get_latest_version(directories):
    if use_semver:
        return get_latest_version_semver(directories)
    else:
        return get_latest_version_generic(directories)


def get_latest_version_semver(directories):
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


def get_latest_version_generic(directories):
    versions = extract_versioned_directory_names(directories)
    if len(versions) == 0:
        return None
    if not same_versioning_schema(versions):
        return None
    return get_latest_from_versions(versions)


def extract_versioned_directory_names(directories):
    versioned_files = []
    for current_directory_name in directories:
        current_version = re.search(VERSION_REGEX, current_directory_name)
        if current_version is None:
            continue
        versioned_files.append(current_version.group(0))
    return versioned_files


def same_versioning_schema(versions):
    if len(versions) < 2:
        return True
    num_parts = list(map(lambda version: len(version.split('.')), versions))
    for i in range(len(num_parts) - 1):
        if num_parts[i] != num_parts[i + 1]:
            return False
    return True


def get_latest_from_versions(versioned_directories):
    if len(versioned_directories) == 0:
        return ''
    elif len(versioned_directories) == 1:
        return versioned_directories[0]
    else:
        last_version = versioned_directories[0]
        for i in range(len(versioned_directories) - 1):
            if is_newer(last_version, versioned_directories[i + 1]):
                last_version = versioned_directories[i + 1]
        return last_version


def is_newer(left, right):
    """Returns true if right is newer than left"""
    left_versions, right_versions = left.split('.'), right.split('.')
    for i in range(len(left_versions)):
        if int(left_versions[i]) < int(right_versions[i]):
            return True
        elif int(left_versions[i]) > int(right_versions[i]):
            return False
    return False


def remove_unless_dry_run(path, directory_name):
    if dry_run:
        print('/'.join([path, directory_name]) + ' will be removed')
    else:
        shutil.rmtree('/'.join([path, directory_name]))

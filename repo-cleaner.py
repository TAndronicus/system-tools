from os.path import isdir
from os import listdir
import re
import shutil
import Constants

dry_run = True

def check_and_clean(path):
    files = listdir(path)
    for file in files:
        if not isdir('/'.join([path, file])):
            return
    last = check_if_versions(files)
    if last is None:
        for file in files:
            check_and_clean('/'.join([path, file]))
    elif len(files) == 1:
        return
    else:
        print('update ' + path.split(Constants.m2_path)[1])
        for file in files:
            if file == last:
                continue
            print(file + ' (newer version: ' + last + ')')
            if not dry_run:
                shutil.rmtree('/'.join([path, file]))


def check_if_versions(files):
    if len(files) == 0:
        return None
    last = ''
    for file in files:
        if re.match(Constants.version_regex, file):
            if last == '':
                last = file
            if len(last.split('.')) == len(file.split('.')):
                for (current, new) in zip(last.split('.'), file.split('.')):
                    if int(new) > int(current):
                        last = file
                        break
                    elif int(new) < int(current):
                        break
            else:
                return None
        else:
            return None
    return last


assert check_if_versions(['1.11.12', '1.13.1']) == '1.13.1'
assert check_if_versions(['1.11.12', '1.11.3']) == '1.11.12'
assert check_if_versions(['1.11.12', '2.10.1']) == '2.10.1'
assert check_if_versions(['1.11.12', '1.13']) is None
assert check_if_versions(['1.11.12']) == '1.11.12'
assert check_if_versions([]) is None

check_and_clean(Constants.m2_path)

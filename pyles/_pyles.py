from sys import exit
from os import listdir, stat
from os.path import isfile, join, splitext
from xattr import getxattr
from biplist import readPlistFromString

FETCH_ATTRIBUTES = ['com.apple.metadata:kMDItemWhereFroms']

def try_get_attribute(file, attribute):
    try:
        xattr = getxattr(file, attribute)
        return (attribute, readPlistFromString(xattr))
    except:
        return None

def try_get_attributes(file, attributes):
    result = []

    for attr in attributes:
        xattr = try_get_attribute(file, attr)

        if xattr is not None:
            result.append(xattr)

    if not result:
        return None

    return result

def run(exts=None, in_path=None):
    file_list = []

    for file in listdir(in_path):
        ext = splitext(file)[-1]
        file_path = join(in_path, file)

        if isfile(file_path) and ext.lower() in exts:
            attributes = try_get_attributes(file_path, FETCH_ATTRIBUTES)

            if attributes is not None:
                entry = (file_path, {
                    'attributes': dict(attributes)
                })

            file_list.append(entry)

    return dict(file_list)

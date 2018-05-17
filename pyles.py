#!/usr/bin/env python
import sys
from os import listdir, stat
from os.path import isfile, join, splitext
from argparse import ArgumentParser, FileType
import pprint
import xattr
import biplist
import json

pp = pprint.PrettyPrinter(indent=2)

###

def try_get_attr(file, attr):
  try:
    return (attr, xattr.getxattr(file, attr))
  except:
    return None

def try_get_attrs(file, attrs):
  result = []
  for a in attrs:
    r = try_get_attr(file, a)
    if r is not None:
      result.append(r)

  if not result:
    return None

  return result

def get_file_stat(file):
  r = stat(file)

  return {
    'size': r.st_size,
    'accessed_at': r.st_atime,
    'modified_at': r.st_mtime,
    'created_at': r.st_ctime
  }

###

def run(args=None):
  if not args:
    print('I need some arguments, man')
    sys.exit(1)

  inpath = args.inpath
  exts = args.exts

  fetch_attrs = ['com.apple.metadata:kMDItemWhereFroms']

  file_attr_list = []

  ###

  for file in [f for f in listdir(inpath) if isfile(join(inpath, f))]:
    (file_base, ext) = splitext(file)

    file_path = join(inpath, file)
    file_extension = ext.lower()

    if not file_extension in exts:
      continue

    attrs = try_get_attrs(file_path, fetch_attrs)

    if attrs is not None:
      file_attr_list.append((file_path, attrs))

  file_attrs = dict(file_attr_list)

  def map_attrs(it):
    tag, value = it

    return (tag, biplist.readPlistFromString(value))

  def map_file(x):
    file, attrs = x
    attrs_ = list(map(map_attrs, attrs))

    return {
      'file': file,
      'stat': get_file_stat(file),
      'attrs': dict(attrs_)
    }

  return list(map(map_file, file_attrs.items()))

###

if __name__ == "__main__":
  parser = ArgumentParser(prog='pyles', description='Collect pyles of data!')

  parser.add_argument('inpath',
                      type=str,
                     help='Path to directory to search through')

  parser.add_argument('-e', '--exts',
                      type=str,
                      default=['jpg', 'png'],
                      nargs='*',
                      help='List of file formats to go through')

  parser.add_argument('-o', '--outfile',
                      type=FileType('w'),
                      nargs='?',
                      default=sys.stdout,
                      help='Save result to the given path')

  args = parser.parse_args()

  def process_ext(ext):
    return '.{}'.format(ext)

  args.exts = list(map(process_ext, args.exts))

  result = run(args)

  args.outfile.write(json.dumps(result))

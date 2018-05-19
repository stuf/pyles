"""Provide argument parsing."""
import sys
from argparse import ArgumentParser, FileType

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

def get_arguments():
    """Get the parsed arguments which the program was called with."""
    return parser.parse_args()

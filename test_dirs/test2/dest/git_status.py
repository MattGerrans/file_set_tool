# import argparse
import pprint
import subprocess
# from app_options import Options
import sys

from print_colors import print_red, print_blue, print_green, print_cyan, print_magenta, print_yellow, print_white
from print_colors import write_red, write_blue, write_green, write_cyan, write_magenta, write_yellow, write_white


def underlined(text):
    return f'{text}\n{"-"*len(text)}'


def get_modified_files_1():
    # Call the 'git status' command and capture the output
    output = subprocess.check_output(['git', 'status', '--porcelain'])

    # Split the output into lines
    lines = output.decode().split('\n')

    # Extract the filenames of modified and added files
    modified_files = []
    added_files = []
    for line in lines:
        if line.startswith('M'):
            filename = line[3:]
            modified_files.append(filename)
        elif line.startswith('A'):
            filename = line[3:]
            added_files.append(filename)

    # Return a dictionary with the modified and added files
    return {'modified': modified_files, 'added': added_files}

def get_modified_files():
    # Call the 'git status' command and capture the output
    output = subprocess.check_output(['git', 'status', '--porcelain', '-uall'])

    # Split the output into lines
    lines = output.decode().split('\n')

    # Extract the filenames of modified, added, and untracked files
    modified_files = []
    added_files = []
    untracked_files = []
    for line in lines:
        line = line.strip()
        if line.startswith('M'):
            filename = line[2:].strip()
            modified_files.append(filename)
        elif line.startswith('A'):
            filename = line[2:].strip()
            added_files.append(filename)
        elif line.startswith('??'):
            filename = line[2:].strip()
            untracked_files.append(filename)

    # Return a dictionary with the modified, added, and untracked files
    return {'modified': modified_files, 'added': added_files, 'untracked': untracked_files}
    
    
def main(args=None):
    error_level = 0
    # args = _get_args()
    # options = Options(options_file_name=args.json_file, args=args)
    info = get_modified_files()
    print_magenta(underlined('Git results:'))
    pprint.pprint(info)
    return error_level


if __name__ == '__main__':
    sys.exit(main())
"""
Todo:
- Option to create file like the fsp file.
- allow specifying a commit as well.
- Add this to file_set_tool; need to make that one command-based...
- gui to unwrap text
"""
import argparse
import json
import os
import pprint
import subprocess

import serializers
from app_options import Options
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


def get_modified_files2():
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


class NotGitDirectoryError(OSError):
    def __init__(self, path=None):
        self.path = path if path else os.curdir
        super().__init__(f"{path} is not a valid Git repository.")


def get_modified_files(git_dir=None, output_file=None, indent=2, as_transfer=False, name='', description='',
                       dest_dir=''):
    # todo: allow specifying directory, but then have to change to that directory and do a try/finally
    # to make sure we come back to the right place.
    current_dir = os.getcwd()
    try:
        if git_dir:
            os.chdir(git_dir)
        # Call the 'git status' command and capture the output
        output = subprocess.check_output(['git', 'status', '--porcelain', '-uall'])
    except subprocess.CalledProcessError:
        raise NotGitDirectoryError(os.path.abspath(os.curdir))
    finally:
        if git_dir:
            os.chdir(current_dir)

    # Split the output into lines
    lines = output.decode().split('\n')

    if lines[0].find('fatal') >= 0:
        raise NotGitDirectoryError(os.path.abspath(os.curdir))

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
            filename = line[3:].strip()
            untracked_files.append(filename)

    # Return a dictionary with the modified, added, and untracked files
    results = {'modified': modified_files, 'added': added_files, 'untracked': untracked_files}

    if as_transfer:
        source_dir = os.path.abspath(os.curdir)
        if not name:
            name = os.path.basename(os.path.abspath(os.curdir))
        results = {
                    "name": name,
                    "description": description,
                    "source_directory": source_dir,
                    "dest_directory": dest_dir,
                    "files": modified_files + added_files + untracked_files,
                    "transmogrifications": []
                  }

    # Write the results to the output file as JSON, if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=indent)

    # Return the results
    return results


def _get_args(raw_args=None):
    raw_args = sys.argv[1:] if raw_args is None else raw_args
    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=os.path.splitext(os.path.basename(sys.argv[0]))[0],
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     fromfile_prefix_chars='@')
    parser.add_argument('file_name', nargs='*', help='The path to the file.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
    parser.add_argument('-t', '--transfer', action='store_true', help='Create transfer (fst) formatted file.')
    parser.add_argument('-n', '--name', help='Name of project.')
    parser.add_argument('-e', '--explication', help='Description.')
    parser.add_argument('-d', '--dest', help='Destination directory.')
    parser.add_argument('-i', '--indent', help='Json indent.')
    # parser.add_argument('-o', '--optional_option')
    # parser.add_argument('-b', '--boolean_option', dest='boolean_option', action='store_true')
    parser.set_defaults(boolean_option=False)
    namespace = parser.parse_args(raw_args)
    # debug overrides: use @args.txt

    return namespace


def main(args=None):
    error_level = 0

    options = Options(args=_get_args())

    gmf_options = {'as_transfer': True if options.transfer else False,
                   'output_file': options.file_name[0] if options.file_name else None,
                   'name': options.name if options.name else None,
                   'description': options.explication if options.explication else None,
                   'dest_dir': options.dest if options.dest else None}
    info = get_modified_files(**gmf_options)

    if options.file_name:
        for file_name in options.file_name:
            serializers.dump_data(info, file_name)
            print_cyan(f'Wrote data to {os.path.abspath(file_name)}.')
    print_magenta(underlined('Git results:'))
    pprint.pprint(info)
    print_yellow(f'options.file_name: {options.file_name}')
    return error_level


if __name__ == '__main__':
    sys.exit(main())
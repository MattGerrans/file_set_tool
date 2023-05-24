r"""

Ubuntu test:
fst -j temp/fst_test/test1.json

C:\code\Python\projects\file_set_tool\src\file_set_tool.py

todo: Perfect installer set up with both setup.py and poetry toml.
todo: Perfect installer set up with poetry toml.
todo: Installer set up as command line tool.
todo: check into git hub
todo: comandify!
todo: add "File Batcher" functions (and substitutions).
"""

import argparse
import file_set_tool_exceptions
import git_status
import munch
import os
import serializers
import sys
import time
from app_options import Options
from ruamel.yaml import YAML

yaml = YAML()
from print_colors import print_blue, print_red, print_green, print_yellow, print_cyan, print_magenta, print_white

script_base_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]


# todo:
#  - Copy a set of files; for existing dest, compare and notify date/size if different;
#    if same, do nothing.
# - options: -y,
# - runtime options y/n/a
# - add FileSetCopier functions.
# - Also, feature to populate the files list in a json from a directory (with optional recurse and patterns)
# - t test option (print all operations, don't do em)
# - Need to automate generation of project/build/whl from a script. Through poetry or setup.py?


def _show_demo_info(data):
    data = munch.munchify(data)
    print_white(f'name:             {data.name}')
    print_cyan(f'description:      {data.description}')
    print_cyan(f'source_directory: {data.source_directory}')
    print_cyan(f'dest_directory:   {data.dest_directory}')
    print_magenta('Files:')
    for file_name in data.files:
        print_green(f'   {file_name}')
    print_magenta(f'transmogrifications')
    for transform in data.transmogrifications:
        print_green(f'   From:          {transform["from"]}')
        print_green(f'   To:            {transform["to"]}')
        print_green(f'   regex:         {transform["regex"]}')
        print_green(f'   file_specific: {transform["file_specific"]}')


def load_file(file_name, encoding='utf-8'):
    with open(file_name, encoding=encoding) as stream:
        return stream.read()


def dump_file(file_name, content, encoding='utf-8'):
    with open(file_name, 'w', encoding=encoding) as stream:
        return stream.write(content)


def check_errors(file_set_data):
    if not os.path.isdir(file_set_data.source_directory):
        raise OSError(f'Error: Source directory "{file_set_data.source_directory}" does not exist.')
    if not file_set_data.source_directory:
        raise file_set_tool_exceptions.InvalidDirectoryError(f'source_directory is not defined.')
    if not os.path.isdir(file_set_data.source_directory):
        raise file_set_tool_exceptions.InvalidDirectoryError(f'source_directory does not exist.')
    if not file_set_data.dest_directory:
        raise file_set_tool_exceptions.InvalidDestinationError(f'dest_directory is not defined.')
    if file_set_data.dest_directory == file_set_data.source_directory:
        raise file_set_tool_exceptions.InvalidDestinationError(f'dest_directory cannot be same as source_directory.')
    for file_name in file_set_data.files:
        full_path = os.path.join(file_set_data.source_directory, file_name)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f'Does not exist: "{full_path}"')


def move_and_update_files(file_set_data):
    directory_set = set()
    file_set_data = munch.munchify(file_set_data)
    check_errors(file_set_data)

    for src_file in file_set_data.files:
        directory_set.add(os.path.dirname(src_file))
        dest_file = os.path.join(file_set_data.dest_directory, src_file)
        dest_dir = os.path.dirname(dest_file)
        src_file = os.path.join(file_set_data.source_directory, src_file)
        content = load_file(src_file)
        for transmogrification in file_set_data.transmogrifications:
            if transmogrification.file_specific or transmogrification.regex:
                # todo: file_specific and regex not implemented yet.
                raise NotImplementedError(f'That feature is not ready yet!')
            t_from, t_to = transmogrification['from'], transmogrification['to']
            previous = content
            content = content.replace(t_from, t_to)
            if previous != content:
                print_yellow(f'   {dest_dir}: transmogrified {t_from} -> {t_to}.')
        os.makedirs(dest_dir, exist_ok=True)
        updated = os.path.isfile(dest_file)
        # todo: if -w or some option, then confirm before stomping.
        created_updated = 'Updated' if updated else 'Created'
        dump_file(dest_file, content)
        print_magenta(f'   --> {created_updated} {dest_file}.')
    if directory_set:
        print_magenta('Updated these directories:')
        for directory in directory_set:
            print_magenta(f'   {directory}')


def update_configuration(configuration, check_environment=False, verbose=False, **vargs):
    cfg = configuration.copy()

    def vp(txt):
        print_cyan(txt)
    if not verbose:
        def vp(txt):
            pass
    
    for key, value in vargs:
        cfg[key] = value
        vp(f'Added specified value "{value}" with key "{key}" to configuration.')
    if check_environment:
        prefix = 'fsp_'
        for key, value in os.environ.items():
            if key.lower().starswith(prefix):
                config_key = key[len('fsp_'):].lower()
                cfg[config_key] = value
                vp(f'Added environment value from variable "{key}" to configuration with key "{config_key}" and value "{value}"')
    return cfg


def _get_args(raw_args=None):
    raw_args = sys.argv[1:] if raw_args is None else raw_args
    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=os.path.splitext(os.path.basename(sys.argv[0]))[0],
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     fromfile_prefix_chars='@')

    parser.add_argument('-j', '--json_file', required=True, help='json file with file set to transmogrify.')

    parser.add_argument('-n', '--name', help='Name.')
    parser.add_argument('-c', '--description', help='Description.')
    parser.add_argument('-s', '--source_directory', help='Source directory.')
    parser.add_argument('-d', '--dest_directory', help='Destination directory.')
    parser.add_argument('-f', '--files', help='File list with relative directories, separated by ";".')
    parser.add_argument('-t', '--test', action='store_true', help='Test mode (will not do operations).')
    parser.add_argument('-g', '--git', action='store_true', help='Get file list from git.')

    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
    parser.set_defaults(boolean_option=False)
    namespace = parser.parse_args(raw_args)
    # debug overrides: use @args.txt

    return namespace


COMMAND_MAP = {
                'git_dirs': None,
                'git_list': None,
                'run_manifest': None,
                'center': None,
                'tile': None,
                'minimize': None,
                'maximize': None,
                'show': None,
                'hide': None
               }


def main(args=None):
    error_level = 0
    try:
        args = _get_args()

        options = Options(options_file_name=args.json_file, args=args)
        verbose = options['verbose'] if 'verbose' in options else False
        if verbose:
            print_magenta(f'args.git is {args.git}')
        json_file = options['json_file']
        data = None

        if 'git' in options and options['git']:
            # todo: in this case source should be inferred to be the git directory.
            name = 'Git Transfer' if options["name"] is None else options["name"]
            year, month, day, hour, minute, second = time.localtime()[:6]
            time_stamp = f'{year}-{month:02}-{day:02}@{hour:02}-{minute:02}-{second:02}'
            dest_dir = fr'c:\temp\auto_{time_stamp}_dest'
            dest_dir = options['dest_directory'] if options['dest_directory'] else dest_dir
            desc = 'Auto generated' if options["description"] is None else options["description"]
            data = git_status.get_modified_files(git_dir=None,
                                                 output_file=json_file,
                                                 as_transfer=options['git'],
                                                 name=name,
                                                 description=desc,
                                                 dest_dir=dest_dir)
            print_magenta(f'Created {json_file}.')
            with open(json_file, encoding='utf-8') as stream:
                lines = [line for line in stream]
            print_green(''.join(lines))
            # raise NotImplementedError('Git option still in progress...')

        if not data:
            data = serializers.load_data(json_file)

        if options['test']:
            _show_demo_info(data)
            print_yellow('These are the options:')
            for key, value in options:
                print_yellow(f'   {key:>20} -> {value}')
        else:
            move_and_update_files(data)
    except:
        error_level = 1

    return error_level


if __name__ == '__main__':
    sys.exit(main())

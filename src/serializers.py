"""
serializers.py

Loads and saves data from json/yaml/toml/ini/cfg/tsv/pickle/txt (fixed width)

Also in Python\projects\spx_test_tool\spx_test_tool\method_info_utils.py.

"""

import json
import os
import toml
from print_colors import print_cyan
from ruamel.yaml import YAML

yaml = YAML()
info = print_cyan

# todo: based on environment variable alternately assign info, debug, warning, error, critical
# to different print_color methods. And for IDLE environment, assign all to print.
# Maybe encapsulate this all into print_color.py...


def dump_data(data, file_name, encoding='utf-8', indent=2, verbose=False):
    """
    Dumps the data to a json/yaml file.
    Other formats can be added if needed: tsv, toml, pickle, ...
    """
    if verbose:
        info(f'Saving data to "{file_name}"...')
    name, ext = [item.lower() for item in os.path.splitext(file_name)]
    with open(file_name, 'w', encoding=encoding) as stream:
        if ext == '.json':
            json.dump(data, stream, indent=indent)
        elif ext == '.yaml':
            yaml.dump(data, stream)
        elif ext == '.toml':
            toml.dump(data, stream)
        elif ext == '.ini':
            raise NotImplementedError('To do - ini.')
        elif ext == '.cfg':
            # Assume ini format?
            raise NotImplementedError('To do - cfg.')
        elif '.tsv':
            raise NotImplementedError('To do - use tsv module.')
        else:
            raise NotImplementedError('To do - fixed width output (assumes data format works for it).')
            # Careful, this makes assumptions about the data format.
    if verbose:
        info(f'Finished writing "{file_name}"')


def load_data(file_name, encoding='utf-8', verbose=False):
    """
    Loads the data from a json/yaml/toml/ini... file.
    Other formats can be added if needed: tsv, toml, pickle, ...
    """
    if verbose:
        info(f'Loading data from "{file_name}"...')
    name, ext = [item.lower() for item in os.path.splitext(file_name)]
    with open(file_name, encoding=encoding) as stream:
        if ext == '.json':
            return json.load(stream)
        elif ext == '.yaml':
            return yaml.load(stream)
        elif ext == '.toml':
            return toml.load(stream)
        elif ext == '.ini':
            raise NotImplementedError('To do - ini.')
        elif ext == '.cfg':
            raise NotImplementedError('To do - cfg.')
        elif ext == '.tsv':
            raise NotImplementedError('To do - use tsv module.')
        elif ext == '.txt' or ext == '.prn':
            raise NotImplementedError('To do - fixed width input (assumes data format works for it).')
        elif '.pickle':
            raise NotImplementedError('To do - use pickle module.')
        else:
            raise NotImplementedError(f'To do - handle "{ext}" format!')
    if verbose:
        info(f'Finished loading "{file_name}"')



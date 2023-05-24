import argparse
import json
import os
from src.app_options import Options


def get_data_dir():
    """
    Returns the absolute path to the data directory.
    """
    return os.path.join(os.path.dirname(__file__), "data")


def get_load_json_file(file_name):
    """
    Tests that a JSON file can be loaded.
    """
    data_dir = get_data_dir()
    with open(os.path.join(data_dir, file_name), "r") as f:
        data = json.load(f)
    return data


def test_toml():
    pass


def test_yaml():
    pass


def test_json():
    options_file_path = os.path.join(get_data_dir(), r'test_options_1.json')
    if not os.path.isfile(options_file_path):
        raise FileNotFoundError(f'Not found: {options_file_path}')
    options = Options(options_file_name=options_file_path, args=argparse.Namespace())
    assert options['name'] == 'Heimdallr'


def test_env_override():
    options_file_path = os.path.join(get_data_dir(), r'test_options_1.json')
    if not os.path.isfile(options_file_path):
        raise FileNotFoundError(f'Not found: {options_file_path}')
    options = Options(options_file_name=options_file_path, args=argparse.Namespace())
    assert options['description'] == 'WAT'


def test_cmd_line_override():
    options_file_path = os.path.join(get_data_dir(), r'test_options_1.json')
    if not os.path.isfile(options_file_path):
        raise FileNotFoundError(f'Not found: {options_file_path}')
    options = Options(options_file_name=options_file_path, args=argparse.Namespace(name='Chet'))
    assert options['name'] == 'Chet'

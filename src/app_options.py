import argparse
import os
import serializers
import sys

from print_colors import print_blue, print_red, print_green, print_yellow, print_cyan, print_magenta


class Options(dict):
    def __init__(self, options_file_name=None, env_prefix='fst_', args=None, verbose=False):
        self.verbose = verbose

        def vprint(msg):
            if verbose:
                print_magenta(msg)

        if options_file_name and os.path.isfile(options_file_name):
            config_data = serializers.load_data(options_file_name)
            for key, value in config_data.items():
                self[key] = value
            # self.update(config_data)
        for key, value in os.environ.items():
            assert isinstance(key, str)
            assert isinstance(env_prefix, str)
            if key.lower().startswith(env_prefix):
                app_key = key.lower()[len(env_prefix):]
                if app_key in self:
                    if self[app_key] != value:
                        vprint(f'Changing FstOptions["{app_key}"] from {self[app_key]} to {value}.')
                else:
                    vprint(f'Adding FstOptions["{app_key}"] = {value}.')
                self[app_key] = value
        if args:
            for key, value in vars(args).items():
                if key in self:
                    if self[key] != value:
                        vprint(f'Changing FstOptions["{key}"] from {self[key]} to {value} from command line.')
                else:
                    vprint(f'Adding FstOptions["{key}"] = {value} from command line.')
                self[key] = value

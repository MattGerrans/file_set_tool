"""
Several simple color print methods.

Usage:

    from print_colors import *
    # then can do calls like
    print_magenta('Hello!')

To use the print_color() method, you also need to import colorama so you can use colorama.Fore to 
specify the color.

from print_colors import print_color, print_red, print_blue, print_green, print_cyan, print_magenta, print_yellow, print_white
from print_colors import write_color, write_red, write_blue, write_green, write_cyan, write_magenta, write_yellow, write_white

"""

import colorama
import sys

colorama.init()


def print_color(color, msg=''):
    print(color + msg + '\33[39m')


def write_color(color, msg=''):
    sys.stdout.write(color + msg + '\33[39m')


def write_red(msg=''): write_color(colorama.Fore.RED, msg)
def write_blue(msg=''): write_color(colorama.Fore.BLUE, msg)
def write_green(msg=''): write_color(colorama.Fore.GREEN, msg)
def write_cyan(msg=''): write_color(colorama.Fore.CYAN, msg)
def write_magenta(msg=''): write_color(colorama.Fore.MAGENTA, msg)
def write_yellow(msg=''): write_color(colorama.Fore.YELLOW, msg)
def write_white(msg=''): write_color(colorama.Fore.WHITE, msg)


def print_red(msg=''): print_color(colorama.Fore.RED, msg)
def print_blue(msg=''): print_color(colorama.Fore.BLUE, msg)
def print_green(msg=''): print_color(colorama.Fore.GREEN, msg)
def print_cyan(msg=''): print_color(colorama.Fore.CYAN, msg)
def print_magenta(msg=''): print_color(colorama.Fore.MAGENTA, msg)
def print_yellow(msg=''): print_color(colorama.Fore.YELLOW, msg)
def print_white(msg=''): print_color(colorama.Fore.WHITE, msg)

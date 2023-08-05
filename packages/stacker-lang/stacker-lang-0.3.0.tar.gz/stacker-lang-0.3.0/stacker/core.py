import argparse
import pprint
import sys

from codecs import open
from os import path

import stacker
from stacker.lang import Stacker
from stacker.errors import StackerFileNotFound

def repl():
    pp = pprint.PrettyPrinter(indent=4)
    interpreter = Stacker()

    def _exit(*args):
        sys.exit()

    def _help(*args):
        pp.pprint(interpreter.scope)

    interpreter.scope.update({
        'help': _help,
        'exit':_exit,
    })

    try:
        input = raw_input
    except NameError:
        pass

    while True:
        user_input = input('=>')
        try:
            interpreter.eval(user_input, interpreter.scope)
        except Exception as e:
            pp.pprint(e)
        finally:
            pp.pprint(list(interpreter.STACK))

def from_file(abs_path):
    stacker = Stacker()
    if not path.exists(abs_path):
        raise StackerFileNotFound('File was not found: {}'.format(abs_path))

    with open(abs_path, 'r') as inp_file:
        for line in inp_file.readlines():
            stacker.eval(str(line), stacker.scope)

    return stacker

def parse_args():
    arg_parser = argparse.ArgumentParser(
        description='Stacker is a stack based programming language.'
    )

    arg_parser.add_argument(
        'file',
        nargs='?',
        type=str
    )

    arg_parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=stacker.__version__
    )

    return arg_parser.parse_args()

def main():
    args = parse_args()
    if args.file:
        filepath = path.abspath(args.file)
        from_file(filepath)
    else:
        repl()



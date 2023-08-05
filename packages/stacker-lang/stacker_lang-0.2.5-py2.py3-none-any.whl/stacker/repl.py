# coding: utf-8
import pprint
import sys
from stacker.lang import Stacker




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


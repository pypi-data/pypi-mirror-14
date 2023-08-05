# coding: utf-8
import pprint
import sys
from stacker.lang import Stacker


def repl():
    pp = pprint.PrettyPrinter(indent=4)
    interpreter = Stacker()

    try:
        input = raw_input
    except NameError:
        pass

    while True:
        user_input = input('=>')
        if user_input == 'exit':
            sys.exit()

        try:
            interpreter.eval(user_input, interpreter.scope)
        except Exception as e:
            print(e)
        finally:
            pp.pprint(list(interpreter.STACK))
            pp.pprint(interpreter.scope)


# coding: utf-8
import re

from collections import deque
from functools import wraps

from stacker.errors import StackerSyntaxError
from stacker.scope import Scope

__all__ = ['Stacker', 'Procedure']


class Procedure (object):
    def __init__(self, inp, name, scope):
        self.inp = inp
        self.name = name
        self.scope = scope

    def expression_list(self):
        return  [exp for exp in self.inp[1:-1].split(';') if exp]


class Stacker (object):

    def __init__(self):
        self.STACK = deque()
        self.scope = self.env()

    def stack_head(self):
        try:
            value = self.STACK[0]
        except IndexError:
            value = None
        return value

    def env(self, **kwargs):

        def _call(*args):
            proc = self.STACK.popleft()
            for exp in proc.expression_list():
                self.eval(exp, proc.scope)

        def _if(*args):
            proc = self.STACK.popleft()
            cond = self.STACK.popleft()
            if cond is False:
                return None
            for exp in proc.expression_list():
                self.eval(exp, proc.scope)

        def _not(*args):
            value = self.STACK.popleft()
            if value is False:
                self.STACK.appendleft(True)
            else:
                self.STACK.appendleft(False)
            return self.STACK

        def _or (*args):
            value1 = self.STACK.popleft()
            value2 = self.STACK.popleft()
            if value1 is False and value2 is False:
                self.STACK.appendleft(False)
            else:
                self.STACK.appendleft(True)
            return self.STACK

        def _eq(*args):
            other = args[0]
            value = self.STACK.popleft()
            out = other == value
            self.STACK.appendleft(out)
            return self.STACK

        def rot(*args):
            value = self.STACK.popleft()
            self.STACK.append(value)
            return self.STACK

        def over(*args):
            value = self.stack_head()
            self.STACK.append(value)
            return self.STACK

        def drop(*args):
            self.STACK.popleft()
            return self.STACK

        def swap(*args):
            value1 = self.STACK.popleft()
            value2 = self.STACK.popleft()
            self.STACK.appendleft(value1)
            self.STACK.appendleft(value2)
            return self.STACK

        def dup(*args):
            value = self.stack_head()
            self.STACK.appendleft(value)
            return self.STACK

        def push(*args):
            self.STACK.appendleft(args[0])
            return self.STACK

        base = {
            'push': push,
            'drop': drop,
            'dup': dup,
            'swap': swap,
            'over': over,
            'rot': rot,
            'eq': _eq,
            'or': _or,
            'not': _not,
            'if': _if,
            'call': _call,
        }

        scope = Scope(None, **base)

        if kwargs:
            scope.update(kwargs)

        return scope

    def parse_procedure(self, inp, scope):
        name_regex = re.compile(r'\w+')
        name = name_regex.match(inp[1:]).group(0)
        return Procedure(inp[len(name) + 2:], name, scope)

    def parser(self, inp, scope):
        if inp is None:
            return None

        inp = inp.strip()
        if inp.startswith('{') and inp.endswith('}'):
            return Procedure(inp, None, scope)
        if inp.startswith('/') and inp.endswith(';}'):
            return self.parse_procedure(inp, scope)
        if len(inp) == 0:
            return None

        funcs = '(' + '|'.join(scope.keys()) + ')'
        matcher = re.compile('{} (\d+|\w+)'.format(funcs))
        expression = matcher.match(inp)
        if not expression:
            raise StackerSyntaxError('invalid syntax: {}'.format(inp))
        return [self.atomizer(atom) for atom in expression.group(0).split()]

    def atomizer(self, atom):
        try:
            value = int(atom)
        except ValueError:
            value = str(atom)
            if value == 'void':
                value = None

            if value == 'false':
                value = False

            if value == 'true':
                value = True

        return value

    def eval(self, inp, scope):
        parsed_inp = self.parser(inp, scope)
        if isinstance(parsed_inp, Procedure):
            if parsed_inp.name is None:
                self.STACK.appendleft(parsed_inp)
            else:
                new_scope = {
                    parsed_inp.name: parsed_inp
                }
                scope.update(new_scope)
        else:
            self.eval_exp(parsed_inp, scope)

    def eval_exp(self, atoms, scope):
        if atoms is None:
            return None

        scoped_variable = scope.find_in_scope(atoms[0])
        if isinstance(scoped_variable, Procedure):
            for exp in scoped_variable.expression_list():
                atoms = self.parser(exp, scoped_variable.scope)
                self.eval_exp(atoms, scope)
            return None
        return scoped_variable(*atoms[1:])


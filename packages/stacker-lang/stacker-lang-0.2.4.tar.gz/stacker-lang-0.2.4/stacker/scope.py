# coding: utf-8
from stacker.errors import StackerUndefinedVariable

class Scope(dict):
    def __init__(self, outer_scope, **kwargs):
        self.outer_scope = outer_scope
        super(Scope, self).__init__(**kwargs)

    def find_in_scope(self, key):
        value = self.get(key, None)
        if value is None and self.outer_scope is not None:
            value = self.outer_scope.get(key, None)

        if value is None:
            raise StackerUndefinedVariable(
                'No variable in scope with key: {}'.format(key)
            )
        return value



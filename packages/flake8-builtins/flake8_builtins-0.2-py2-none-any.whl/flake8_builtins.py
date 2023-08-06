# -*- coding: utf-8 -*-
import ast
import inspect
import sys


WHITE_LIST = [
    '__name__',
    '__doc__',
    'credits',
]


if sys.version_info >= (3, 0):
    import builtins
    BUILTINS = [
        a[0]
        for a in inspect.getmembers(builtins)
        if a[0] not in WHITE_LIST
    ]
else:
    import __builtin__
    BUILTINS = [
        a[0]
        for a in inspect.getmembers(__builtin__)
        if a[0] not in WHITE_LIST
    ]


class BuiltinsChecker(object):
    name = 'flake8_builtins'
    version = '0.1'
    assign_msg = 'B001 "{0}" is a python builtin and is being shadowed, ' \
                 'consider renaming the variable'
    argument_msg = 'B002 "{0}" is used as an argument and thus shadows a ' \
                   'python builtin, consider renaming the argument'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        for statement in ast.walk(self.tree):
            value = None
            if isinstance(statement, ast.Assign):
                value = self.check_assignment(statement)

            elif isinstance(statement, ast.FunctionDef):
                value = self.check_function_definition(statement)

            if value:
                for line, offset, msg, rtype in value:
                    yield line, offset, msg, rtype

    def check_assignment(self, statement):
        for element in statement.targets:
            if isinstance(element, ast.Name) and \
                    element.id in BUILTINS:

                line = element.lineno
                offset = element.col_offset
                yield (
                    line,
                    offset,
                    self.assign_msg.format(element.id),
                    type(self)
                )

    def check_function_definition(self, statement):
        if sys.version_info >= (3, 0):
            for arg in statement.args.args:
                if isinstance(arg, ast.arg) and \
                        arg.arg in BUILTINS:

                    line = arg.lineno
                    offset = arg.col_offset
                    yield (
                        line,
                        offset,
                        self.argument_msg.format(arg.arg),
                        type(self)
                    )
        else:
            for arg in statement.args.args:
                if isinstance(arg, ast.Name) and \
                        arg.id in BUILTINS:

                    line = arg.lineno
                    offset = arg.col_offset
                    yield (
                        line,
                        offset,
                        self.argument_msg.format(arg.id),
                        type(self)
                    )

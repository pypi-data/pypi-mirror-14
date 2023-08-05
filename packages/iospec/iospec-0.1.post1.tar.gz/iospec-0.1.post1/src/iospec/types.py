import sys


# Share memory for these string constants
TYPE, DATA = 'type', 'data'
INPUT, OUTPUT = 'input', 'output'


class Node(dict):
    """
    A dictionary that access keys as attributes.
    """
    __slots__ = ['parent']

    def __init__(self, *args, parent=None, **kwds):
        super().__init__(*args, **kwds)
        self._setattr('parent', parent)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        self[sys.intern(attr)] = value

    def _setattr(self, attr, value):
        super().__setattr__(attr, value)


class TemplateNode(Node):
    def inputs(self, idx=None):
        if idx is None:
            return [self.inputs(idx) for idx in range(len(self.cases))]
        return self.cases[idx].inputs()

    def source(self):
        return '\n\n'.join(case.source() for case in self.cases)


#
# Test cases
#
class TestCaseNode(Node):
    """We call a single interaction/run of a program with a set of user inputs
    a "test case".

    There are different types of case nodes, either "error-*", for representing
    failed executions, "input-*" for representing input-only specifications and
    finally "io-*", that represents both inputs and outputs of a successful
    program run.
    """

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.setdefault('data', [])

    def inputs(self):
        raise NotImplementedError

    def source(self):
        raise NotImplementedError


class ErrorTestCase(TestCaseNode):
    """
    Error test cases are created using a decorator::

        @timeout 1 sec
            a regular block of input/output interactions

            @error
            a block of messages displayed to stderr

        @segfault
            a regular block of input/output interactions

            @error
            a block of messages displayed to stderr

        @exception 1
            a regular block of input/output interactions

            @error
            a block of messages that should be displayed to stderr

    The need for error blocks is twofold. It may be the case that the desired
    behavior of a program is to indeed display an error message. It is also
    necessary in order to use the IOSpec format to *describe* how a program
    actually ran.

    The type attribute of an ErrorTestCase is one of 'error-timeout',
    'error-segfault' or 'error-exception'. In all cases, the error block
    consists of a data section that has all regular io interactions just like
    an io block and
    """

    def source(self):
        return '@error'


class IoTestCase(TestCaseNode):
    def inputs(self):
        return [x.data for x in self.data if x.type.startswith('input')]

    def source(self):
        src = []
        for line in self.data:
            if line.type == OUTPUT:
                src.append(line.data)
            else:
                src.append(line.data + '\n')
        return ''.join(src)



class InputTestCase(TestCaseNode):
    pass


class Atom:
    """Base class for all atomic elements"""
    type = 'atom'

    def __init__(self, data):
        self.data = str(data)

    def __str__(self):
        return self.data

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.data)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.data == other.data
        return NotImplemented

    def source(self):
        """Expand node as an iospec source code."""

        return self.data


class In(Atom):
    """Plain input string"""

    type = 'input'

    def source(self):
        return '<%s>\n' % self.data


class Out(Atom):
    """Plain output string"""

    type = 'output'
    escape_chars = {
        '<': '\\<',
        '$': '\\$',
    }

    def __init__(self, data, escape=False):
        if escape:
            for c, esc in self.escape_chars.items():
                data = data.replace(esc, c)
            super().__init__(data)

    def source(self):
        data = self.data

        if '\n' in self:
            data = '\n'.join('|' + line for line in data.splitlines())
        for c, esc in self.escape_chars.items():
            data = data.replace(c, esc)
        return data


class Command(Atom):
    def __init__(self, name, args, generator, data=None):
        super().__init__(data)
        self.name = name
        self._args = args
        self._generator = generator

    def generate(self):
        return self._generator(self._args)
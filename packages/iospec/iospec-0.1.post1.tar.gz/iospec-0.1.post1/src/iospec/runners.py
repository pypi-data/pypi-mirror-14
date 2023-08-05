import io
import sys
import copy
import functools
from collections import deque
from iospec.parser import Node, INPUT, OUTPUT

__all__ = ['expand_inputs', 'IoObserver']


def expand_inputs(tree, size=0):
    """
    Expand all computed inputs

    Parameters
    ----------

    tree:
        A parse tree resulting from :func:`iospec.parse`.
    size:
        The target size for the number of test cases. In might be impossible to
        reach this number and thus this function may return a number of test
        cases that either smaller or larger than this number.


    Returns
    -------

    A new parse tree with all computable input blocks expanded to random values.


    Examples
    --------

    Consider the simple iospec example that have a silly computed input

    >>> from iospec import parse_string
    >>> from pprint import pprint
    >>> iodata = '''
    ... @command
    ... def foo(arg):
    ...     return 'computed value'
    ...
    ... foo: $foo
    ... '''

    Now let us parse this example. Notice that the second node is a of type
    'input-computed'.

    >>> tree = parse_string(iodata)
    >>> pprint(tree.cases)                                  # doctest: +ELLIPSIS
    [{'data': [{'data': 'foo: ', 'type': 'output'},
               {'args': None,
                'generate': <function ...>,
                'name': 'foo',
                'type': 'input-computed'}],
      'type': 'io-computed'}]

    After expanding inputs, all cases and interactions are normalized to the
    non-computed versions, which can be more easily compared with a program run.

    >>> tree = expand_inputs(tree)
    >>> pprint(tree.cases)
    [{'data': [{'data': 'foo: ', 'type': 'output'},
               {'data': 'computed value', 'type': 'input'}],
      'type': 'io-simple'}]

    """
    # Assign the number of expanded cases for each object
    test_count = [[case, 1] for case in tree.cases]
    if size > len(test_count):
        test_count = redistribute_test_counts(test_count, size)

    # Run these extra test-cases and expand inputs
    cases = []
    for case, num in test_count:
        for _ in range(num):
            if case.type not in ('io-simple', 'input-plain'):
                case = ExpandInputs.expand_block(case, tree)
            cases.append(case)

    result = Node({k: copy.deepcopy(v) for (k, v) in tree.items()
                                       if k != 'cases'})
    result.cases = cases
    return result


class ExpandInputs:
    """
    This class is a namespace that implements related functions for the
    expand_inputs() function.
    """

    node_whitelist = ['output', 'input']

    @classmethod
    def expand_block(cls, block, context):
        """Expand all computable inputs of the given input block and return a
        computed block.

        This command expands io-* blocks to type 'io-plain' and all input-* blocks
        to type 'input-plain'.
        """

        attr = 'expand_' + block.type.replace('-', '_')
        try:
            method = getattr(cls, attr)
        except AttributeError:
            raise ValueError('block type is not supported: %s' % block.type)
        return method(block, context)

    @classmethod
    def expand_io_computed(cls, block, context):
        new = copy.deepcopy(block)
        for idx, node in enumerate(new.data):
            if node.type == 'input-computed':
                node = Node(type='input', data=node.generate())
                new.data[idx] = node
            elif node.type in cls.node_whitelist:
                pass
            else:
                raise ValueError('non-supported type: %s' % node.type)
        new.type = 'io-simple'
        return new


class IoObserver:
    """
    Implements functions that helps to track the flow of inputs and outputs in
    a Python session.

    It implements an ``input`` and a ``print`` methods that works as drop-in
    replacements for the corresponding Python's functions.

    Example
    -------

    We create a new observer and export its print and input methods to a
    dictionary namespace.

    >>> io_obs = IoObserver(['foo'])
    >>> namespace = {
    ...     'print': io_obs.print,
    ...     'input': io_obs.input,
    ... }
    >>> exec('''
    ... name = input('What is your name? ')
    ... print('Hello %s' % name)
    ... ''', namespace)

    All interactions with print and Xinput were recorded. We can obtain a list
    of interaction using the flush() method. This cleans the recording data
    and returns what was already registered by the observer.

    >>> from pprint import pprint
    >>> pprint(io_obs.flush())
    [{'data': 'What is your name? ', 'type': 'output'},
     {'data': 'foo', 'type': 'input'},
     {'data': 'Hello foo\\n', 'type': 'output'}]
    >>> io_obs.interactions()
    []
    """

    __print = staticmethod(print)
    __input = staticmethod(input)

    class EmptyInputError(RuntimeError):
        pass

    def __init__(self, inputs=()):
        self._stream = []
        self._inputs = deque()
        if isinstance(inputs, str):
            self.append_input(inputs)
        else:
            for value in inputs:
                self.append_input(value)

    def flush(self):
        """Flush all stored input/output interactions and return a list with
        all registered activities."""

        result = self._stream
        self._inputs = deque()
        self._stream = []
        return result

    def interactions(self):
        """Return a list of interactions that happened so far."""

        return list(self._stream)

    @functools.wraps(print)
    def print(self, *args, sep=' ', end='\n', file=None, flush=False):
        if not (file is None or file is sys.stdout):
            self.__print(*args, sep=sep, end=end, file=file, flush=flush)
        else:
            file = io.StringIO()
            self.__print(*args, sep=sep, end=end, file=file, flush=flush)
            self.write_output(file.getvalue())

    @functools.wraps(input)
    def input(self, prompt=None):
        if prompt is not None:
            self.write_output(prompt)
        return self.next_input()

    def write_output(self, data):
        """This function should be called instead of (or in addition to) writing
        data to the standard output."""

        if self._stream and self._stream[-1].type == OUTPUT:
            self._stream[-1].data += data
        else:
            self._stream.append(Node(type=OUTPUT, data=data))

    def write_input(self, data):
        """This function should be called instead of (or in addition to) writing
        a line of text to the standard output.

        The input data should end in a newline."""

        if not data.endswith('\n'):
            msg = 'received an incomplete line of input: %r' % data
            raise RuntimeError(msg)

        self._stream.append(Node(type=INPUT, data=data[:-1]))

    def next_input(self):
        """Consume the next input on the list of inputs"""

        try:
            value = self._inputs.popleft()
        except ValueError:
            raise self.EmptyInputError('input list is empty')
        self.write_input(value + '\n')
        return value

    def append_input(self, input):
        """Add a new input value to the end of list.

        If the string has a newline, it will be split into different input
        values, one per line.
        """

        if not isinstance(input, str):
            raise TypeError('expect strings, got %r' % input)
        lines = input.splitlines(keepends=False)
        self._inputs.extend(lines)

    def extend_inputs(self, seq):
        """Append sequence of inputs to the end of the input list"""

        for inpt in seq:
            self.append_input(inpt)

    def prepend_input(self, input):
        """Like append_input, but add inputs to the beginning of the queue."""

        for line in reversed(input.splitlines(keepends=False)):
            self._inputs.appendleft(line)

    def clear_inputs(self):
        """Clear the list of pending inputs."""

        self._inputs = deque()

    def inputs(self):
        """Return a list of pending inputs."""

        return list(self._inputs)


class IoExampleObserver(IoObserver):
    """An IoObserver that keeps comparing interactions with a given example
    run.

    It fails as soon as the interaction starts to contradict the example.
    Users should not manipulate inputs in instances of this class unless
    they really know what they are doing."""

    class UnexpectedOutputError(RuntimeError):
        pass

    class UnexpectedOutputDataError(RuntimeError):
        pass

    def __init__(self, template):
        super().__init__()
        self.replace_template(template)

    def replace_template(self, template):
        """Replace the current reference example and update the input list."""

        inputs = [node.data for node in template if node.type == INPUT]
        self.clear_inputs()
        self.append_input(inputs)
        self.template = template

    def write_output(self, data):
        super().write_output(data)

        # Check if outputs are consistent with template
        idx = len(self._stream) - 1
        cur_data = self._stream[idx].data
        ref_node = self.template[idx]
        if ref_node != OUTPUT:
            raise self.UnexpectedOutputError
        elif not ref_node.data.startswith(cur_data):
            raise self.UnexpectedOutputDataError(cur_data, ref_node.data)

if __name__ == '__main__':
    from doctest import testmod
    testmod()

    from iospec.parser import parse_string
    from pprint import pprint
    st = '''
@command
def foo(arg):
    return 'foo'

foo: $foo
'''
    x = parse_string(st)
    y = expand_inputs(x)
    #pprint(y)


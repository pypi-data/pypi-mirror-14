#
# Tests random input generators and runners
#
import io
import pytest
from iospec import parse, parse_string


def test_open_file():
    src = 'foo<bar>'
    assert parse(io.StringIO(src)) == parse_string(src)


def test_simple_io():
    tree = parse_string('foo<bar>\nfoobar')
    case = tree.cases[0].data
    assert case[0].data == 'foo'
    assert case[1].data == 'bar'
    assert case[2].data == 'foobar'


def test_multiline_with_pipes():
    tree = parse_string(
        '|foo\n'
        '|\n'
        '|bar'
    )
    assert len(tree.cases) == 1
    assert len(tree.cases[0].data) == 1
    assert tree.cases[0].data[0].data == 'foo\n\nbar'


def test_computed_input():
    tree = parse_string('foo$name(10)')
    session = tree.cases[0].data
    assert len(session) == 2
    assert session[0].type == 'output'
    assert session[1].type == 'input-computed'
    assert session[1].name == 'name'
    assert session[1].args == '10'


def test_import_command():
    tree = parse_string(
        '@import math\n'
        '@from random import choice\n'
        '@command\n'
        'def foo(arg):'
        '    return math.sqrt(choice([1]))')
    assert tree.commands.foo.generate('') == 1


if __name__ == '__main__':
    pytest.main()
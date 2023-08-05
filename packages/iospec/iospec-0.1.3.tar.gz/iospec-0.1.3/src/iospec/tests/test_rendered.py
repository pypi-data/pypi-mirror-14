import pytest
from iospec import parse_string


# Some iospec examples
RENDER_BACK_SOURCES = """# simple example
foo: <bar>
foobar

# simple computed
foo: $name
foobar

# computed with argument
foo: $name(10)
foobar

# imports
@import math
@from math import sqrt

# python command definition
@command
def foo(*args):
    return 1

# input blocks
@input
    foo
    $name
    $int(10)

# inline input
@input foo;$name;$int(10)

# plain input blocks
@plain
    foo
    $foobar
    $baz

# inline plain
@plain foo;$foobar;tl\;dr
""".split('\n\n')


@pytest.fixture(params=RENDER_BACK_SOURCES)
def source(request):
    lines = request.param.splitlines()
    return '\n'.join(lines[1:])


def test_simple_render_back(source):
    parsed = parse_string(source)
    assert source.strip() == parsed.source().strip()


if __name__ == '__main__':
    pytest.main('test_rendered.py')
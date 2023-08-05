import re
from collections import deque
from iospec.commands import commands, wrapped_command
from iospec.make_commands import commands as make_commands
from iospec.types import *

__all__ = ['parse', 'parse_string']


def parse(file):
    """Parse the content of file.

    This function accepts file-like objects and a string with a path.
    
    Returns the parsing tree as a dictionary-like structure.
    """
    if isinstance(file, str):
        with open(file) as F:
            data = F.read()
        return parse_string(data)
    return parse_string(file.read())
    
    
def parse_string(text):
    """Parse a string of iospec data."""

    # Extract all blocks
    ctx = TemplateNode(
        globals_ns={},
        commands=Node(commands.copy()),
        make_commands=Node(make_commands.copy()),
    )
    group_iterator = group_blocks(enumerate(text.splitlines()))
    blocks = []
    for group in group_iterator:
        block = parse_group(group, group_iterator, ctx)
        if block is not None:
            blocks.append(block)

    # Fuse consecutive outputs
    for block in blocks:
        if block.type.startswith('io'):
            idx = 1
            data = block.data
            while idx < len(data):
                if data[idx].type == 'output' and data[idx - 1].type == 'output':
                    data[idx - 1].data += '\n' + data.pop(idx).data
                else:
                    idx += 1

    del ctx['globals_ns']
    return Node(ctx, cases=blocks)
    

def group_blocks(lines):
    """Groups lines of each session block together.
    
    The input is a list of (line_index, line) pairs. Return an iterator over a 
    list of lines in each group."""
    
    session = deque()
    lines = deque(lines)
    lines.append((None, ''))
    
    while lines:
        idx, line = lines.popleft()
        
        # Whitespace and comments divide chunks
        if not line or line.isspace() or line.startswith('#'):
            if not session:
                continue
            
            data = yield session
            while data is not None: 
                yield data
                data = yield session
               
            session = deque()
        else:
            session.append((idx, line))              


def parse_group(lines, groups, ctx):
    """Parse all lines in group and return the parsed tree."""
    
    stream = []
    result = IoTestCase(type='io-plain', data=stream)
    
    # Block-start flags
    first_line = lines[0][1]
    if first_line.startswith('<<'):
        return parse_input_session(lines, groups)
    elif first_line.startswith('@command'):
        return parse_input_command(lines, groups, ctx)
    elif first_line.startswith('@import') or first_line.startswith('@from'):
        return parse_import(lines, groups, ctx)

    while lines:
        idx, line = lines.popleft()

        # Line-start flags
        if line.startswith('|'):
            line = line[1:]
                
        # Process line
        match = output_re.match(line)
        if match:
            out, line = match.groups()
            stream.append(Out(out, escape=True))

        match = input_re.match(line)
        if match:
            stream.append(normalize_input(match.group(1), ctx))
            continue

        match = computed_input_re.match(line)
        if match:
            result.type = 'io-computed'
            name, args = match.groups()
            stream.append(normalize_computed_input(name, args, ctx))
                
    return result
 
    
#
# Parse special blocks
#        
def parse_input_session(lines, groups):
    inputs = []
    lines[0] = lines[0][0], lines[0][1][3:]
    for _, line in lines:
        line = line.rstrip()
        if line.endswith(';') and not line.endswith('\\;'):
            line = line[:-1]
        inputs.extend(line.split(';'))

    idx = 0
    while idx < len(inputs):
        if inputs[idx].endswith('\\'):
            inputs[idx] = '%s;%s' % (inputs[idx][:-1], inputs.pop(idx + 1))
        else:
            idx += 1
    return Node(type='inputs', data=inputs)
    
    
def parse_input_command(lines, groups, ctx):
    idx, line = lines.popleft()
    if line.strip() != '@command':
        raise SyntaxError('invalid command in line %s: %s' % (idx, line))
    
    groups.send(lines)
    source = consume_python_code_block(groups)
    
    # Execute source and collect python object
    namespace = {}
    exec(source, ctx.globals_ns, namespace)
    if len(namespace) != 1:
        data = ['    ' + line for line in source.splitlines()]
        data = '\n'.join(data)
        raise SyntaxError('python source does not define a single object:\n' + data)
    name, obj = namespace.popitem()
    ctx.globals_ns[name] = obj
    ctx.commands[name] = wrapped_command(obj)

    
def parse_import(lines, groups, ctx):
    idx, line = lines.popleft()
    if lines:
        groups.send(lines)
    exec(line[1:], ctx.globals_ns)


def consume_python_code_block(groups):
    """Return a node that collects the source code for a python class or 
    function definition. Return a string of source code"""
    
    lines = next(groups)
    idx, line = lines.popleft()
    head = line
    
    # Consume all decorators
    while line.startswith('@'):
        idx, line = lines.popleft()
        head += '\n' + line
        
    if not line.startswith('def') or line.startswith('class'):
        raise SyntaxError('expect function or class definition on line: %s' % idx)
    
    # Add all lines to source
    groups.send(lines)
    data = consume_indented_code_block(groups)
    return'%s\n%s' % (head, data)

    
def consume_indented_code_block(groups):
    """Consume all indented lines in groups and return the source string"""
    
    source = []
    for lines in groups:
        go = True
        while lines:
            idx, line = lines.popleft()
            if line and line[0].isspace():
                source.append(line)
            else:
                lines.appendleft((idx, line))
                go = False
                break
        if not go:
            break
    if lines:                
        groups.send(lines)
        
    return '\n'.join(source)
    
    
#
# Parse lines of regular input blocks
#
def normalize_input(data, ctx):
    return Node(type=INPUT, data=data)

    
def normalize_computed_input(name, args, ctx):
    obj = ctx.commands[name]
    parsed_args = obj.parse(args)

    return Node(
        type='input-computed',
        name=name,
        args=args,
        generate=lambda: obj.generate(parsed_args),
    )
    
       
#
# Token definitions
#
output_re = re.compile(r'''
^(
    (?:    
        [^<\$]*    # Match any non-$/< sequence
        (?:\\.)*   # Match any escaped characters
    )*             # Perform zero or more of these matches
)(.*)$
''', flags=re.VERBOSE)

input_re = re.compile(r'^<(.*)>\s*$')
computed_input_re = re.compile(r'^\$([a-zA-Z]+)(?:[(](.*)[)])?\s*$')
enumerated_input_re = re.compile(r'^\$([0]+)\s*$')
input_value_re = re.compile(r'''
^(
    (?:
        [^;]*
        (?:\\.)*
    )*
)\;''', flags=re.VERBOSE)


if __name__ == '__main__':
    from pprint import pprint
    st = '''
<< foo;bar;
baz\\;
;
ham;
tl\\;dr
baz\\;
'''
    st = '''
Foo: $name
'''
    pprint(parse_string(st))

#!/usr/bin/env python

# Example code for programatically calling the purdy library and showing a
# console based code snippet

from purdy.actions import (Append, Wait, Suffix, SuffixTypewriter,
    Replace, ReplaceTypewriter)
from purdy.content import Code
from purdy.ui import SplitScreen

screen = SplitScreen(top_starting_line_number=10)
top = screen.top
bottom = screen.bottom

source = """\
@decorator
def foo(x):
    \"\"\"Multi-line
    doc string
    \"\"\"
    for index in range(1, x):
        blah = '''
            thing'''
        # about to print
        print(index)
"""
code = Code(text=source)

source = """\
>>> a = 1
>>> b = 2
>>> c = 3
"""
repl = Code(text=source)

actions = [
    Append(top, code),
    Append(bottom, repl),
    Wait(),
    Suffix(top, 1, 's'),
    Suffix(top, 1, ' # append'),
    Suffix(top, 2, ' # append'),
    Suffix(top, 3, ' more string now'),
    Suffix(top, 5, ' # append'),
    Suffix(top, 6, ' # append'),
    Suffix(top, 7, '  inside blah mline'),
    Suffix(top, 8, ' # append'),
    Suffix(top, 9, ' more comment'),
    Suffix(top, 10, ' # append'),
    Wait(),
    SuffixTypewriter(bottom, 2, '9'),
    Wait(),
]

blob1 = Code(text='>>> d = 4')
blob2 = Code(text='>>> e = 5')

actions.extend([
    Replace(bottom, 3, blob1),
    Wait(),
    SuffixTypewriter(bottom, 1, '56789'),
    Wait(),
    Suffix(bottom, 1, '333'),
    SuffixTypewriter(bottom, 1, '444'),
    Wait(),
    ReplaceTypewriter(bottom, 2, blob2),
])

screen.run(actions)

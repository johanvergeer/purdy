#!/usr/bin/env python

# Example code for programatically calling the purdy library and showing a
# console based code snippet

from purdy.actions import AppendAll
from purdy.content import CodeBlob
from purdy.ui import Screen

screen = Screen(show_line_numbers=True)
code_box = screen.code_box
blob = CodeBlob('../display_code/simple.py', 'con')

actions = [
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
    AppendAll(code_box, blob),
]

screen.run(actions)

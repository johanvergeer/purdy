#!/usr/bin/env python

# Example code for programatically calling the purdy library and showing a
# console based code snippet

from purdy.actions import AppendAll
from purdy.content import CodeFile
from purdy.ui import Screen

screen = Screen()
code_box = screen.code_box
blob = CodeFile('../display_code/console.py', 'con')
action = AppendAll(code_box, blob)
screen.run([action])

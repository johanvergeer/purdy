#!/usr/bin/env python

# Example code for showing a top with code and a bottom with console

from purdy.actions import (AppendAll, AppendTypewriter, Highlight, StopMovie,
    Wait)
from purdy.content import CodeFile
from purdy.settings import settings
from purdy.ui import SplitScreen

settings['movie_mode'] = 2

py_code = CodeFile('../display_code/code.py', 'py3')
con_code = CodeFile('../display_code/simple.repl', 'con')

screen = SplitScreen(settings, show_top_line_numbers=True,
    top_auto_scroll=False)
py_box = screen.top_box
con_box = screen.bottom_box

actions = [
    AppendAll(py_box, py_code),
    Wait(),
    AppendTypewriter(con_box, con_code),
    Wait(),
    StopMovie(screen),
    Wait(),
    Highlight(py_box, 4, True),
    Wait(),
    Highlight(con_box, 3, True),
    Wait(),
    Highlight(py_box, 4, False),
]

screen.run(actions)

#!/usr/bin/env python

### Example purdy library code
#
# Demonstrates movie mode

from purdy.actions import AppendTypewriter
from purdy.settings import settings
from purdy.content import Code
from purdy.ui import SimpleScreen

settings['movie_mode'] = 200

screen = SimpleScreen(settings)
code_box = screen.code_box
blob = Code('../display_code/console.repl')
actions = [
    AppendTypewriter(code_box, blob),
]

if __name__ == '__main__':
    screen.run(actions)

"""
Actions
-------

Library users specify a series of actions that turn into the presentation
animations in the Urwid client.  An action is similar to a slide in a slide
show, except it can both present and change lines of code on the screen.

All purdy library programs have the following basic structure:

.. code-block:: python

    screen = Screen(...)
    actions = [ ... ]
    screen.run(actions)

Each action gets translated into a series of steps defined in the
:mod:`purdy.animation` module.
"""
import random
from copy import copy

from pygments.token import Generic, Token

from purdy.animation import cell
from purdy.parser import CodePart, CodeLine, LEXERS, parse_source, token_is_a

# =============================================================================
# Single Code Blob Actions
# =============================================================================

class Append:
    """Adds the content of a :class:`purdy.content.Code` object to the end of
    a :class:`purdy.ui.CodeBox`.
    """
    def __init__(self, code_box, code):
        self.code_box = code_box
        self.code = code

    def steps(self):
        lines = parse_source(self.code.source, self.code.lexer)
        steps = [cell.AddRows(self.code_box, lines), ]

        return steps


class Insert:
    """Inserts the content of a :class:`purdy.content.Code` object to a
    specified line in a :class:`purdy.ui.CodeBox`. Pushes content down, 
    inserting at "1" is the beginning of the list. Position is 1-indexed
    """
    def __init__(self, code_box, position, code):
        self.code_box = code_box
        self.code = code
        self.position = position

    def steps(self):
        lines = parse_source(self.code.source, self.code.lexer)
        steps = [cell.InsertRows(self.code_box, self.position, lines), ]

        return steps


class Replace:
    """Replaces one or more lines of a :class:`purdy.ui.CodeBox` using the
    content of a :class:`purdy.content.Code` object.
    """
    def __init__(self, code_box, position, code):
        self.code_box = code_box
        self.code = code
        self.position = position

    def steps(self):
        lines = parse_source(self.code.source, self.code.lexer)
        steps = [cell.ReplaceRows(self.code_box, self.position, lines), ]

        return steps


class Remove:
    """Removes one or more lines of a :class:`purdy.ui.CodeBox`.
    """
    def __init__(self, code_box, position, size):
        self.code_box = code_box
        self.position = position
        self.size = size

    def steps(self):
        return [cell.RemoveRows(self.code_box, self.position, self.size), ]


class Clear:
    """Clears the contents of a :class:`purdy.ui.CodeBox`."""
    def __init__(self, code_box):
        self.code_box = code_box

    def steps(self):
        return [cell.Clear(self.code_box), ]

# =============================================================================
# Source Based Actions
# =============================================================================

class Suffix:
    """Adds the provided text to the end of an existing line in a
    :class:`purdy.ui.CodeBox`.
    """
    def __init__(self, code_box, position, source):
        self.code_box = code_box
        self.position = position
        self.source = source

    def steps(self):
        return [cell.SuffixRow(self.code_box, self.position, self.source), ]

# =============================================================================
# Typewriter Actions
# =============================================================================

class TypewriterBase:
    continuous = [Generic.Prompt, Generic.Output, Generic.Traceback]

    @property
    def delay_until_next_letter(self):
        typing_delay = self.code_box.screen.settings['delay'] / 1000
        variance = self.code_box.screen.settings['delay_variance']

        vary_by = random.randint(0, 2 * variance) - variance
        return typing_delay + (vary_by / 1000)


class TypewriterStep(TypewriterBase):
    def _line_to_steps(self, line, position):
        steps = []

        # --- Skip animation for "output" content
        first_token = line.parts[0].token
        is_console = LEXERS.is_lexer_console(self.code.lexer)

        if is_console and not token_is_a(first_token, Generic.Prompt):
            # in console mode only lines with prompts get typewriter
            # animation, everything else is just added directly
            return [cell.InsertRows(self.code_box, position, line), ]

        # --- Typewriter animation
        # insert a blank row first with contents of line changing what is on
        # it as animation continues
        dummy_parts = [CodePart(Token, ''), ]
        row_line = CodeLine(dummy_parts, self.code.lexer)
        step = cell.InsertRows(self.code_box, position, row_line)
        steps.append(step)

        current_parts = []
        num_parts = len(line.parts)
        for count, part in enumerate(line.parts):
            if part.token in self.continuous:
                # part is a chunk that gets output all together, replace the
                # dummy line with the whole contents
                current_parts.append(part)
                row_line = CodeLine(copy(current_parts), self.code.lexer)
                step = cell.ReplaceRows(self.code_box, position, row_line)
                steps.append(step)

                if part.token == Generic.Prompt:
                    # stop animation if this is a prompt, wait for keypress
                    steps.append( cell.CellEnd() )
            else:
                new_part = CodePart(part.token, '')
                current_parts.append(new_part)

                typewriter = ''
                for letter in part.text:
                    typewriter += letter
                    new_part = CodePart(part.token, typewriter)
                    current_parts[-1] = new_part
                    output_parts = copy(current_parts)

                    # If not last step in animation, add a cursor to the line
                    is_last_part = (count + 1 == num_parts)
                    is_last_letter = (len(typewriter) == len(part.text))
                    if not (is_last_part and is_last_letter):
                        output_parts.append( CodePart(Token, '\u2588') )

                    row_line = CodeLine(output_parts, self.code.lexer)
                    step = cell.ReplaceRows(self.code_box, position, row_line)
                    steps.append(step)

                    steps.append(cell.Sleep(self.delay_until_next_letter))

        return steps


    def steps(self):
        steps = []

        lines = parse_source(self.code.source, self.code.lexer)
        for count, line in enumerate(lines):
            line_steps = self._line_to_steps(line, self.position + count)
            steps.extend(line_steps)

        return steps


class AppendTypewriter(TypewriterStep):
    """Adds the content of a :class:`purdy.content.Code` object to a
    :class:`purdy.ui.CodeBox`.
    """
    def __init__(self, code_box, code):
        self.code_box = code_box
        self.code = code
        self.position = 1


class InsertTypewriter(TypewriterStep):
    """Insert the content of a :class:`purdy.content.Code` object at the given
    position into a :class:`purdy.ui.CodeBox` using a typewriter animation.
    """
    def __init__(self, code_box, position, code):
        self.code_box = code_box
        self.code = code
        self.position = position


class ReplaceTypewriter(TypewriterStep):
    """Replaces one or more lines in a :class:`CodeBox` with the contents of a 
    :class:`purdy.ui.CodeBox` using a typewriter animation.
    """
    def __init__(self, code_box, position, code):
        self.code_box = code_box
        self.code = code
        self.position = position

    def steps(self):
        # Override TypewriterStep, need to remove the line before inserting a
        # new one
        steps = []

        lines = parse_source(self.code.source, self.code.lexer)
        for count, line in enumerate(lines):
            # remove old line
            step = cell.RemoveRows(self.code_box, self.position + count)
            steps.append(step)

            # typewriter insert in place of removed line
            line_steps = self._line_to_steps(line, self.position + count)
            steps.extend(line_steps)

        return steps


class SuffixTypewriter(TypewriterBase):
    """Adds the provided text to the end of an existing line in using a
    typewriter animation :class:`purdy.ui.CodeBox`.
    """
    def __init__(self, code_box, position, source):
        self.code_box = code_box
        self.position = position
        self.source = source

    def steps(self):
        steps = []
        for count, letter in enumerate(self.source):
            cursor = False
            if count + 1 != len(self.source):
                cursor = True

            steps.extend([
                cell.SuffixRow(self.code_box, self.position, letter, cursor),
                cell.Sleep(self.delay_until_next_letter),
            ])

        return steps

# =============================================================================
# Presentation Actions
# =============================================================================

class Highlight:
    """Cause one or more lines of code to have highlighting turned on or
    off"""

    def __init__(self, code_box, spec, highlight_on):
        """Constructor

        :param code_box: CodeBox to perform on
        :param spec: either a string containing comma separated and/or hyphen
                     separated integers (e.g. "1,3,7-9") or a list of integers
                     specifying the lines in the code box to highlight. Line
                     numbers are 1-indexed
        :param highlight_on: True to turn highligthing on, False to turn it
                             off
        """
        self.code_box = code_box
        self.highlight_on = highlight_on

        if isinstance(spec, str):
            from purdy.scribe import range_set_to_list

            self.numbers = range_set_to_list(spec)
        else:
            self.numbers = spec

    def steps(self):
        return [ cell.HighlightLines(self.code_box, self.numbers,
            self.highlight_on) ]

# =============================================================================
# Control Actions
# =============================================================================

class Wait:
    """Causes the animations to wait for a key press before continuing."""
    def steps(self):
        return [cell.CellEnd(), ]


class StopMovie:
    """Causes the presentation :class:`purdy.ui.Screen` to exit movie mode"""
    def steps(self):
        return [cell.StopMovie(), ]

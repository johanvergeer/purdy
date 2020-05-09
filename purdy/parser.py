"""
Parser
-------

This contains methods and classes to manager parsing of code
"""
from copy import copy
from collections import namedtuple

from pygments.lexers import PythonConsoleLexer, PythonLexer, BashSessionLexer
from pygments.token import String, Token

# =============================================================================
# Pygments Token Management
# =============================================================================

LexerHolder = namedtuple('LexerHolder', ['name', 'lexer', 'description',
    'is_console'])

class LexerContainer:
    def __init__(self):
        holders = [
            LexerHolder('con',  PythonConsoleLexer(), 'Python Console', True), 
            LexerHolder('py3',  PythonLexer(), 'Python 3', False),
            LexerHolder('bash', BashSessionLexer(), 'Bash Console', True),
        ]
        self._lexers = {h.name:h for h in holders}
        self._reverse_lookup = {h.lexer.__class__:h for h in holders}

    @property
    def names(self):
        return self._lexers.keys()

    @property
    def choices(self):
        return ', '.join([f'"{h.name}" ({h.description})' for h in \
            self._lexers.values()])

    def get_lexer(self, name):
        return self._lexers[name].lexer

    def is_lexer_console(self, lexer):
        ### Returns true if the lexer passed in is a console style lexer
        holder = self._reverse_lookup[lexer.__class__]
        return holder.is_console

    def detect_lexer(self, source):
        if source.startswith('>>> ') or '\n>>> ' in source:
            return self.get_lexer('con')
        elif source.startswith('#!'):
            first, _, _ = source.partition('\n')
            if 'python' in first:
                return self.get_lexer('py3')
            elif any(item in first for item in ['/sh', '/bash']):
                return self.get_lexer('bash')
        elif source.startswith('$ ') or '\n$ ' in source:
            return self.get_lexer('bash')

        return self.get_lexer('py3')

LEXERS = LexerContainer()

# -----------------------------------------------------------------------------

def token_is_a(token1, token2):
    """Returns true if token1 is the same type as or a child type of token2"""
    if token1 == token2:
        return True

    parent = token1.parent
    while(parent != None):
        if parent == token2:
            return True

        parent = parent.parent

    return False


def token_ancestor(token, ancestor_list):
    """Tokens are hierarchical, in some situations you need to translate a
    token into one from a known list, e.g. turning a
    "Token.Literal.Number.Integer" into a "Number". This method takes a token
    and a list of approved ancestors and attempts to make the map. If no
    ancestor is found then a generic "Token" object is returned

    :param token: token to translate into an approved ancestor
    :param ancestor_list: list of approved ancestor tokens
    """
    if token in ancestor_list:
        return token

    # token not in the approved list, search its ancestors
    token = token.parent
    while(token != None):
        if token in ancestor_list:
            return token

        token = token.parent

    # something went wrong with our lookup, return the default
    return Token

# ===========================================================================
# Purdy Code Representation 
# ===========================================================================

CodePart = namedtuple('CodePart', ['token', 'text'])

class CodeLine:
    def __init__(self, parts, lexer, line_number=-1, highlight=False):
        """Represents a displayed line of code.

        :param text: plain text version of line
        :param parts: list of :code:`CodePart` objects that correspond to 
                       this line of code
        :param line_number: line number for the line, -1 for off (default)
        :param highlight: True if this line is currently highlighted
        """
        # too many bugs caused by a change to the parts list after the
        # CodeLine was created, copy the damn thing so it is internal only
        self.parts = copy(parts)       
        self.line_number = line_number
        self.highlight = highlight
        self.lexer = lexer

        self.text = ''.join([part.text for part in parts])

    def __str__(self):
        num = ''
        if self.line_number > -1:
            num = f'{self.line_number:3} '
        return f'CodeLine("{num}{self.text}")'

    def __repr__(self):
        return self.__str__()


def parse_source(source, lexer):
    """Parses blocks of source text, returning a list of :class:`CodeLine` 
    objects.
    """
    parser = _Parser(lexer)
    parser.parse(source)

    return parser.lines


class _Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lines = []

    def parse(self, content):
        self.parts = []
        for token_type, text in self.lexer.get_tokens(content):
            if text == '\n':
                self.newline_handler(token_type)
            elif text == '':
                # tokenizer sometimes puts in empty stuff, skip it
                continue
            elif token_is_a(token_type, String) and '\n' in text:
                self.string_handler(token_type, text)
            else:
                self.default_handler(token_type, text)

    def newline_handler(self, token):
        # hit a CR, time to create a new CodeLine object
        if not self.parts:
            part = CodePart(token, '')
            self.parts = [part, ]

        self.lines.append( CodeLine(self.parts, self.lexer) )

        # reset to start the next set of tokens
        self.parts = []

    def string_handler(self, token, text):
        # String tokens may be multi-line
        for line in text.splitlines(True):
            part = CodePart(token, line.rstrip('\n'))
            self.parts.append(part)

            if line[-1] == '\n':
                self.lines.append( CodeLine(self.parts, self.lexer) )
                self.parts = []

    def default_handler(self, token, text):
        if text[-1] == '\n':
            # there is a \n at the end of the text, need to rebuild it
            # without it, then create the CodeLine object
            part = CodePart(token, text.rstrip('\n'))
            self.parts.append(part)

            # text caused a CR, create a new CodeLine object
            self.lines.append( CodeLine(self.parts, self.lexer ) )

            # reset to start the next group of tokens
            self.parts = []
        else:
            part = CodePart(token, text)
            self.parts.append(part)

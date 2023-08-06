# Copyright (C) 2016 Jeandre Kruger
#
# This file is part of s2scm.
#
# s2scm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# s2scm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with s2scm.  If not, see <http://www.gnu.org/licenses/>.

import sys, re

class Symbol:
    """Represents a symbol."""
    def __init__(self, s):
        self.str = s.lower()

    def __repr__(self):
        return "Symbol(%r)" % self.str

def is_symbol_char(char, first = False):
    if first:
        return bool(re.match(r'[a-zA-Z!$%&*+./:<=>?@^_~-]', char))
    return bool(re.match(r'[a-zA-Z0-9!$%&*+./:<=>?@^_~-]', char))

def read_symbol(char, f = sys.stdin):
    """Read a symbol from the file f.

    Start with the character char."""
    s = ''

    while True:
        s += char

        next_char = f.read(1)

        if is_symbol_char(next_char):
            char = next_char
        else:
            # Unread the character.
            f.seek(-1, 1)
            return Symbol(s)

def read_num(char, f = sys.stdin):
    """Read a number from the file f.

    Start with the character char."""
    s = ''

    read_decimal = False

    while True:
        s += char

        next_char = f.read(1)

        if re.match(r'[0-9]', next_char):
            char = next_char
        elif re.match(r'[0-9.]', next_char) and not read_decimal:
            char = next_char
            read_decimal = True
        else:
            # Unread the character.
            f.seek(-1, 1)

            if read_decimal:
                return float(s)
            else:
                return int(s)

def read_string(f = sys.stdin):
    """Read a string from the file f."""
    # Escape sequences
    escapes = {
        'a': '\a',
        'b': '\b',
        'f': '\f',
        'n': '\n',
        'r': '\r',
        't': '\t',
        'v': '\v'
    }

    s = ''

    while True:
        char = f.read(1)

        if char == '':
            raise SyntaxError('Unexpected EOF, expected "')

        if char == '"':
            break

        if char == '\\':
            # Escape sequence
            escape = f.read(1)

            if escape == '':
                raise SyntaxError('Unexpected EOF after \\ in string')

            if escape in escapes:
                s += escapes[escape]
            else:
                s += escape
        else:
            s += char

    return s

def read_hash(f = sys.stdin):
    """Read a boolean or character from the file f."""
    char = f.read(1)

    if char == '':
        raise SyntaxError('Unexpected EOF after #')

    if char == 't':
        return True
    elif char == 'f':
        return False
    elif char == '\\':
        # Character
        ch = f.read(1)
        if ch == '':
            raise SyntaxError('Unexpected EOF after #\\')
        return ch
    else:
        raise SyntaxError('Unexpected #%s' % char)

def read_token(f = sys.stdin):
    """Read a single token from the file f."""
    char = f.read(1)

    if char == '':
        return ''
    elif re.match(r'[\n\t\v ]', char):
        return read_token(f)
    elif char == '(' or char == ')':
        return char
    elif char == '"':
        return read_string(f)
    elif char == '#':
        return read_hash(f)
    elif is_symbol_char(char, True):
        return read_symbol(char, f)
    elif re.match(r'[0-9]', char):
        return read_num(char, f)
    else:
        raise SyntaxError('Unexpected character %s' % char)

def read_list(f = sys.stdin):
    """Read a list from the file f."""
    tok = read_token(f)

    if tok == '':
        raise SyntaxError('Unexpected EOF, expected )')
    elif tok == ')':
        return []
    elif tok == '(':
        lst = read_list(f)
        return [lst] + read_list(f)
    else:
        return [tok] + read_list(f)

def read(f = sys.stdin):
    """Read a single S-Expression from the file f."""
    tok = read_token(f)

    if tok == '(':
        return read_list(f)
    elif tok == ')':
        raise SyntaxError('Unexpected )')
    else:
        return tok

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

import kurt

def arg(t, name):
    """Get a custom block argument of type t and name name."""
    shapes = {
        'n': 'number',
        's': 'string'
    }
    return kurt.Insert(shapes[t], name = name)

def proc_return(val = ''):
    return kurt.Block('append:toList:', val, 'return stack')

def proc_get_return(blocktype):
    return [kurt.Block('setVar:to:', 'return', kurt.Block('getLine:ofList:', 'last', 'return stack')),
            kurt.Block('deleteLine:ofList:', 'last', 'return stack')]

def proc_add(blocktype):
    return [proc_return(kurt.Block('+', kurt.Block('getParam', 'x'), kurt.Block('getParam', 'y')))]
def proc_sub(blocktype):
    return [proc_return(kurt.Block('-', kurt.Block('getParam', 'x'), kurt.Block('getParam', 'y')))]
def proc_mul(blocktype):
    return [proc_return(kurt.Block('*', kurt.Block('getParam', 'x'), kurt.Block('getParam', 'y')))]
def proc_div(blocktype):
    return [proc_return(kurt.Block('/', kurt.Block('getParam', 'x'), kurt.Block('getParam', 'y')))]

def proc_say(blocktype):
    return [kurt.Block('say:duration:elapsed:from:',
                       kurt.Block('getParam', 's'), kurt.Block('getParam', 'duration')),
            proc_return()]

# All the builtin procedures
procedures = {
    'get return': (kurt.CustomBlockType('stack', ['get return']), proc_get_return),
    '+':          (kurt.CustomBlockType('stack', ['+', arg('n', 'x'), arg('n', 'y')]), proc_add),
    '-':          (kurt.CustomBlockType('stack', ['-', arg('n', 'x'), arg('n', 'y')]), proc_sub),
    '*':          (kurt.CustomBlockType('stack', ['*', arg('n', 'x'), arg('n', 'y')]), proc_mul),
    '/':          (kurt.CustomBlockType('stack', ['/', arg('n', 'x'), arg('n', 'y')]), proc_div),
    'say':        (kurt.CustomBlockType('stack', ['say', arg('s', 's'), arg('n', 'duration')]), proc_say)
}

def init_builtins(sprite):
    """Add all the builtin procedures to the sprite sprite."""
    for proc in procedures:
        script = [kurt.Block('procDef', procedures[proc][0])] + procedures[proc][1](procedures[proc][0])
        sprite.scripts.append(kurt.Script(script))

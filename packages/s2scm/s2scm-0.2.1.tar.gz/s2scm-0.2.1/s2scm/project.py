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
from procedures import procedures, init_builtins
from reader import read

class ArgumentsError(Exception):
    pass

def compile_proc_call(call, sprite, script):
    """Compile the procedure call call."""
    script.append(kurt.Block(procedures[call[0].str][0],
                             *map(lambda x: compile_sexpr(x, sprite), call[1:])))
    script.append(kurt.Block(procedures['get return'][0]))

    return kurt.Block('readVariable', 'return')

def special_form_if(sexpr, sprite, script = None):
    if len(sexpr) > 4:
        raise ArgumentsError('Too many arguments for if')
    elif len(sexpr) < 3:
        raise ArgumentsError('Not enough arguments for if')

    if script is None:
        script = sprite.scripts[0]

    if len(sexpr) == 3:
        then_clause = []
        ret = compile_sexpr(sexpr[2], sprite, then_clause)
        then_clause.append(kurt.Block('setVar:to:', 'ifVal', ret))
        script.append(kurt.Block('doIf', compile_sexpr(sexpr[1], sprite),
                                 then_clause))
    else:
        then_clause = []
        else_clause = []
        then_ret = compile_sexpr(sexpr[2], sprite, then_clause)
        else_ret = compile_sexpr(sexpr[3], sprite, else_clause)
        then_clause.append(kurt.Block('setVar:to:', 'ifVal', then_ret))
        else_clause.append(kurt.Block('setVar:to:', 'ifVal', else_ret))
        script.append(kurt.Block('doIfElse', compile_sexpr(sexpr[1], sprite),
                                 then_clause, else_clause))

    return kurt.Block('readVariable', 'ifVal')

special_forms = {
    'if': special_form_if
}

def compile_sexpr(sexpr, sprite, script = None):
    """Compile a single S-Expression and return a list of kurt.Block."""
    if script is None:
        script = sprite.scripts[0]

    if isinstance(sexpr, list) and sexpr != []:
        if sexpr[0].str in special_forms:
            return special_forms[sexpr[0].str](sexpr, sprite, script)
        else:
            return compile_proc_call(sexpr, sprite, script)
    else:
        return sexpr

def compile_project(infile, outfile):
    """Compile Scheme to Scratch.

    Take the Scheme file infile as input and outfile as output."""

    project = kurt.Project()

    sprite = kurt.Sprite(project, 'Sprite')
    sprite.scripts.append(kurt.Script([kurt.Block("whenGreenFlag")]))
    init_builtins(sprite)

    f = open(infile, 'r')

    while True:
        sexpr = read(f)
        if sexpr == '':
            break
        compile_sexpr(sexpr, sprite)

    f.close()

    project.sprites.append(sprite)

    project.save(outfile)

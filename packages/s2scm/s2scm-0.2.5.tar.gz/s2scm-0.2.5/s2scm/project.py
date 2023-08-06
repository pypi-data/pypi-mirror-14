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

# Script new blocks should be appended to.
current_script = None

# Current environment.
current_env = []

# Number of continuations.
cont_count = 0

def get_env_vals(env):
    return map(lambda x: x[1], env)

def get_env_inserts(env):
    return map(lambda x: x[0], env)

def continuation_type(env):
    global cont_count
    t = kurt.CustomBlockType('stack', ['continuation_%d' % cont_count] + get_env_inserts(env))
    cont_count += 1
    return t

def compile_proc_call(call, sprite, script):
    """Compile the procedure call call."""
    script.append(kurt.Block(procedures[call[0].str][0],
                             *map(lambda x: compile_sexpr(x, sprite), call[1:])))
    script.append(kurt.Block(procedures['get return'][0]))

    return kurt.Block('readVariable', 'return')

def special_form_define(sexpr, sprite, script = None):
    global current_script

    if len(sexpr) > 3:
        raise ArgumentsError('Too many arguments for define')
    elif len(sexpr) < 3:
        raise ArgumentsError('Not enough arguments for define')

    if script is None:
        script = current_script

    name = sexpr[1].str
    val = compile_sexpr(sexpr[2], sprite, script)
    current_env.append((kurt.Insert('string', name = name), val))
    cont_type = continuation_type(current_env)
    cont_call = kurt.Block(cont_type, *get_env_vals(current_env))
    cont = [kurt.Block('procDef', cont_type)]

    script.append(cont_call)

    sprite.scripts.append(kurt.Script(cont))

    # Start adding new blocks at the continuation.
    current_script = sprite.scripts[-1]

    return kurt.Block('getParam', name)

def special_form_if(sexpr, sprite, script = None):
    if len(sexpr) > 4:
        raise ArgumentsError('Too many arguments for if')
    elif len(sexpr) < 3:
        raise ArgumentsError('Not enough arguments for if')

    if script is None:
        script = current_script

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
    'define': special_form_define,
    'if':     special_form_if
}

def compile_sexpr(sexpr, sprite, script = None):
    """Compile a single S-Expression and return a list of kurt.Block."""
    if script is None:
        script = current_script

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

    global current_script

    project = kurt.Project()

    sprite = kurt.Sprite(project, 'Sprite')
    sprite.scripts.append(kurt.Script([kurt.Block("whenGreenFlag")]))
    current_script = sprite.scripts[0]
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

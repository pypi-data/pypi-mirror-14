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

from distutils.core import setup

setup(
    name = "s2scm",
    version = "0.1.1",
    description = "Compile Scheme to MIT Scratch",
    author = "Jeandre Kruger",
    author_email = "Unknown",
    url = "https://github.com/Jonathan50/s2scm",
    packages = [ "s2scm" ],
    requires = [ "kurt" ]
)

=====
s2scm
=====
.. image:: https://travis-ci.org/Jonathan50/s2scm.svg?branch=master
    :target: https://travis-ci.org/Jonathan50/s2scm

Compile Scheme source code to `MIT Scratch <http://scratch.mit.edu>`_ projects.

s2scm uses `kurt <http://github.com/tjvr/kurt>`_ by blob8108.

------
Status
------
s2scm is currently only able to compile very simple Scheme programs.

s2scm aims for R\ :sup:`5`\ RS compliance.

------------
Installation
------------
::

   pip install s2scm

If ``pip`` is for Python 3, you'll then need to use ``pip2`` instead.

-----
Usage
-----
::

   python -m s2scm infile.scm outfile.sb2

If ``python`` is Python 3, you'll then need to use ``python2`` instead.

------
Manual
------
The GNU Texinfo manual source is stored in ``doc/s2scm.texi``.

You can read it online here: http://pythonhosted.org/s2scm/

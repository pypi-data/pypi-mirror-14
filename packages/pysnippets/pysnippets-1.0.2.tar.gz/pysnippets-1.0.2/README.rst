==========
pysnippets
==========

Python Snippets

Installation
============

::

    pip install pysnippets


Usage
=====

::

    Python 2.7.5 (default, Mar  9 2014, 22:15:05)
    Type "copyright", "credits" or "license" for more information.

    IPython 2.2.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: import pysnippets.dictsnippets as dsnippets

    In [2]: dsnippets.filter({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'])
    Out[2]: {'c': 3, 'd': 4}

    In [3]: dsnippets.filter({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'], exec_eval=False)
    Out[3]: {'c': 3, 'd': '4'}

    In [4]: dsnippets.gets({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'])
    Out[4]: [3, 4]

    In [5]: dsnippets.gets({'a': 1, 'b': 2, 'c': 3}, ['c', 'd:4'], exec_eval=False)
    Out[5]: [3, '4']

    In [6]:


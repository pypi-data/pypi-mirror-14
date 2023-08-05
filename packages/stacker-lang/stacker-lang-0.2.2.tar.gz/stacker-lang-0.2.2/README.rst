Stacker-lang
============

A quick and dirty attempt at a stack oriented language
``````````````````````````````````````````````````````

.. image:: https://travis-ci.org/djds23/stacker-lang.svg?branch=master
    :target: https://travis-ci.org/djds23/stacker-lang

Install with: ``pip install stacker-lang``

This should install the bin ``stacker-repl`` command in your current environment.

The repl will look something like this::

   =>help void
   {   'drop': <function drop at 0x10997eb90>,
       'dup': <function dup at 0x10997ec80>,
       'eq': <function _eq at 0x10997ea28>,
       'exit': <function _exit at 0x10997ed70>,
       'help': <function _help at 0x10997ede8>,
       'not': <function _not at 0x10997e398>,
       'or': <function _or at 0x10997e9b0>,
       'over': <function over at 0x10997eb18>,
       'push': <function push at 0x10997ecf8>,
       'rot': <function rot at 0x10997eaa0>,
       'swap': <function swap at 0x10997ec08>}
   =>push 9
   [9]
   =>push 10
   [10, 9]
   =>push 1000
   [1000, 10, 9]
   =>rot void
   [10, 9, 1000]
   =>rot void
   [9, 1000, 10]
   =>drop void
   [1000, 10]

Check this project out on PyPi_.

.. _PyPi: https://pypi.python.org/pypi/stacker-lang


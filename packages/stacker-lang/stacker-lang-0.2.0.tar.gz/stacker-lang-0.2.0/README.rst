Stacker-lang
============

A quick and dirty attempt at a stack oriented language
``````````````````````````````````````````````````````

.. image:: https://travis-ci.org/djds23/stacker-lang.svg?branch=master
    :target: https://travis-ci.org/djds23/stacker-lang

To test, run: ``python -m unittest discover tests --verbose``

Install with: ``python setup.py install``

This should install the bin ``stacker-repl`` in your current environment.

The repl will look something like this::

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


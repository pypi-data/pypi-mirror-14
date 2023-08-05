===============================
faz
===============================

.. image:: https://badge.fury.io/py/faz.png
    :target: http://badge.fury.io/py/faz

.. image:: https://travis-ci.org/hmartiniano/faz.png?branch=master
        :target: https://travis-ci.org/hmartiniano/faz

.. image:: https://pypip.in/d/faz/badge.png
        :target: https://pypi.python.org/pypi/faz


Faz is a data workflow tool heavily inspired in .. _Drake: https://github.com/Factual/drake

The intended use is combining data treatment scripts in bash, python, ruby (or anything else, with a little coding) into a single text file.

The name "faz" is portuguese for "do" or "make".

The various steps can be separated into tasks, with defined inputs and outputs. Dependencies between the tasks are determined from inputs and outputs of every task. The program executes all tasks in the appropriate order, checking for the existence of output and input files.


Why?
----

* Because I like Drake but can't stand the startup time of java.
* Because I can (actually to see if I can, but it turns out I can).

Features
--------

* simple but robust functionality
* easy to use and extend (the code, minus the tests, is around 300 lines of python)
* fast startup time (compared to Drake)
* Documentation: https://faz.readthedocs.org.

Installation
------------

Using pypi

.. code-block:: bash

  pip install faz


Usage
-----

>From the command line, just type

.. code-block:: bash

  faz

without arguments, the program will read the tasks from a file called "fazfile".
If you want to use another filename, just give that as an argumento to the program

.. code-block:: bash

  faz <filename>

to get a list of command line arguments type

.. code-block:: bash

  faz -h

Task file basics
----------------

The task file is a plain text file, with a syntax similar to Drake input files.
The following is an example with two tasks

.. code-block:: python

  # file1 <-
  touch file1

  # file2 <- file1
  cat file1 > file2

Lines starting with "#" and having the symbols "<-" signal a task.
On the left of the "<-" is a (comma separated) list of the files produced by the task.
On the right are the task dependencies, the files needed to run that task.
In the above example the first task has no dependencies, and produces a file called "file1".
The second task has "file1" as a dependency, and has as output a file called "file2".

The outputs and inputs and inputs of each task are used by the program to estabilish the order 
by which the tasks have to be run, and if they need to be run. In the example above, if a file
called "file1" was already present in the directory the program was run, the first task would not be executed.

The code sections, are all the lines in betweeen the two task lines. 
In these two tasks, they are just are just plain bash commands but could be, for example, python code

.. code-block:: python

  # file1 <-
  touch file1

  # file2 <- file1 :python
  f1 = open("file1")
  text = file1.read()
  f2 = open("file2", "w")
  f2.write(text)

note that, in the second task, there's an extra option ":python", wich indicates to the program that
the code from this task is python code.
Options are a list of (comma separated) keywords follwing the ":", and must be placed after the inputs.






History
-------

0.1.0 (2014-01-11)
---------------------

* First release.

0.1.1 (2015-03-20)
---------------------

* Bug fixes.

0.1.2 (2015-10-17)
---------------------

* Project name change.

0.1.3 (2016-03-26)
---------------------

* NextworkX dependency removed.






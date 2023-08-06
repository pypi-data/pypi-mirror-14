===========================
Ultra Fast Template Library
===========================

This project provides a library which allows for very flexible and fast template renderings at the expense of security.
It uses python code to generate variables which are then substituted in a string.Template.

Examples
========

Here's a basic example:

.. code-block:: python

  from uftlib import UFTemplate

  initial = """import datetime
  def f(x):
      return x*x
  
  def getnow():
      return str(datetime.datetime.now())
  
  a = 0
  b = 100
  i = 0"""
  
  oncycle = """a += 3
  i += 1
  s = f(i)
  b += a
  now = getnow()"""

  template = """Now = ${now}
  Render nr. ${i}
  f(${i}) = ${s}
  b = ${b}
  We live in ${where}"""

  tpl = UFTemplate(initial, oncycle, template, where="Indonezia")
  for text in tpl.render_many(1):
      print(text)

We should get the following output:

::

  Now = 2015-08-25 16:09:07.015948
  Render nr. 1
  f(1) = 1
  b = 103
  We live in Indonezia

We can reset the template to it's initial state and obtain the same results:

.. code-block:: python

  tpl.reset()
  for text in tpl.render_many(2):
      print(text)

You should get the following output:

::

  Now = 2015-08-25 16:09:07.016970
  Render nr. 1
  f(1) = 1
  b = 103
  We live in Indonezia
  Now = 2015-08-25 16:09:07.017298
  Render nr. 2
  f(2) = 4
  b = 109
  We live in Indonezia


Warning
=======

You can put any kind of python code in the initial section, such as open and read web pages,
connect to databases, read and parse other files, but this comes at the expense of security,
as malitious code will be run on the same environment as the interpreter. This is a tradeoff
which is not advantageous for all projects and needs, so use this library at your own expense.


Flexibility
===========

The three required arguments (initial, oncycle and template) may be stored on a database and
may be retrieved by multiple programs in the network, which parallelize and distribute the task.
Most templating engines store some of the logic in the template and some of it in the code which
calls the template render, leading to a big mess. Use uftlib to cut that corner.

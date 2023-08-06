wordpad
+++++++

.. image:: https://travis-ci.org/scisco/wordpad.svg?branch=master
    :target: https://travis-ci.org/scisco/wordpad

Adds padding to the right or left of a given string

Installation
============

::

    $ pip install wordpad

or::

    $ python setup.py install


Tests
=====

::

    $ python setup.py test


Example
=======

::

  >>> from wordpad import pad
  >>> pad('1', 3)
  '001'
  >>> pad('1', 3, direction='right')
  '100'
  >>> pad('his', 4, char='t')
  'this'


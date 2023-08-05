.. include:: definitions.txt

.. _`install`:

Download
========

.. raw:: html
   :file: download.html


Install
=======

Install using: ::

	$ python setup.py install
	
This command will also install the requirements pyparsing_, numpy_, setproctitle_, termcolor_, if they are not already installed.
	
unit tests
----------

It is a good idea to run the unit tests using the command: ::

    $ python setup.py nosetests

(This assume that nose_ is installed.)



.. _pyparsing: http://pyparsing.wikispaces.com/ 
.. _numpy: http://numpy.scipy.org/
.. _setproctitle:  http://code.google.com/p/py-setproctitle/
.. _termcolor: http://pypi.python.org/pypi/termcolor/
.. _nose: http://code.google.com/p/python-nose/


About
=====

Do you have thousands of files that you need to run the same program on? Are xargs, GNU parallel, and any of the million workflow management systems not working out for you? This command line tool may be of assistance.

The package also includes parallel implementations of the Python :code:`map` and :code:`imap` functions and a few handy bits and pieces for logging.

Examples
========

To create a directory full of text files from a directory full of text files, with every instance of the string "Tony" in the files replaced with the string "Malcolm":

.. code:: bash

  mpimap -i /path/to/input/dir -o /path/to/output/dir sed 's/Tony/Malcolm/g'

To unzip a directory of gzipped files into a different directory using 2048 cores you could run:

.. code:: bash

  mpirun -n 2048 mpimap -i /path/to/input/dir -o /path/to/output/dir gzip -dc {i}.gz 

To create a tarball full of :code:`*.rst` files from a tarball full of :code:`*.md` files using 4 cores:

.. code:: bash

  mpirun -n 4 mpimap -i /path/to/input.tar.gz -o /path/to/output.tar.gz cp {i}.rst {o}.md

Note that the above command only works if your reStructedText files are also valid Markdown files. A more realistic (but less portable) example would use, for instance, pandoc.

.. .. note:: 
  :code:`mpimap` relies on the input and output directories (or a temp directory for tarred input) being visible to all of the processes, probably via a shared file system.

To calculate :math:`\pi` in parallel in Python (the slow way):

.. code:: python

  from random import random
  from mpiutils.dispatcher import imap, am_dispatcher

  def am_in_circle(i):
      x = 2*random() - 1
      y = 2*random() - 1
      return x*x + y*y < 1

  num_points = 100000
  num_in_circle = 0
  for in_circle in imap(am_in_circle, xrange(num_points)):
      num_in_circle += in_circle

  if am_dispatcher():
      print 4.*num_in_circle/num_points

Installation
============

.. code:: bash

  pip install mpiutils

Documentation
=============

Link to the real documentation here.

Support
=======

Issue tracker: https://bitbucket.org/bkaehler/mpiutils/issues

Contribute
==========

Source Code: https://bitbucket.org/bkaehler/mpiutils/

License
========

GPLv3 or any later version.

.. Contents:

.. .. toctree::
   :maxdepth: 2

..   modules

.. Indices and tables
   ==================

.. * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`


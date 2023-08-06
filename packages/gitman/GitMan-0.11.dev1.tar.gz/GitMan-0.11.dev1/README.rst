| |Build Status|
| |Coverage Status|
| |Scrutinizer Code Quality|
| |PyPI Version|
| |PyPI Downloads|

Getting Started
===============

GitMan is a language-agnostic "dependency manager" using Git. It aims to
serve as a submodules replacement and provides advanced options for
managing versions of nested Git repositories.

Requirements
------------

-  Python 3.4+
-  Latest version of Git (with `stored
   credentials <http://git-dependency-manager.info/setup/git/>`__)
-  OSX/Linux (with a decent shell for Git)

Installation
------------

GitMan can be installed with pip:

.. code:: sh

    $ pip install gitman

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/jacebrowning/gitman.git
    $ cd gitman
    $ python setup.py install

Setup
-----

Create a configuration file (``gitman.yml`` or ``.gitman.yml``) in the
root of your working tree:

.. code:: yaml

    location: vendor
    sources:
    - repo: https://github.com/kstenerud/iOS-Universal-Framework
      dir: framework
      rev: Mk5-end-of-life
    - repo: https://github.com/jonreid/XcodeCoverage
      dir: coverage
      rev: master
      link: Tools/XcodeCoverage

Ignore the dependency storage location:

.. code:: sh

    $ echo vendor >> .gitignore

Basic Usage
===========

See the available commands:

.. code:: sh

    $ gitman --help

Updating Dependencies
---------------------

Get the latest versions of all dependencies:

.. code:: sh

    $ gitman update

which will essentially:

#. create a working tree at *root*/``location``/``dir``
#. fetch from ``repo`` and checkout the specified ``rev``
#. symbolically link each ``location``/``dir`` from *root*/``link`` (if
   specified)
#. repeat for all nested working trees containing a configuration file
#. record the actual commit SHAs that were checked out (with ``--lock``
   option)

where ``rev`` can be:

-  all or part of a commit SHA: ``123def``
-  a tag: ``v1.0``
-  a branch: ``master``
-  a ``rev-parse`` date: ``'develop@{2015-06-18 10:30:59}'``

Restoring Previous Versions
---------------------------

Display the specific revisions that are currently installed:

.. code:: sh

    $ gitman list

Reinstall these specific versions at a later time:

.. code:: sh

    $ gitman install

Deleting Dependencies
---------------------

Remove all installed dependencies:

.. code:: sh

    $ gitman uninstall

Advanced Options
================

See the full documentation at
`git-dependency-manager.info <http://git-dependency-manager.info/interfaces/cli/>`__.

.. |Build Status| image:: https://travis-ci.org/jacebrowning/gitman.svg?branch=develop
   :target: https://travis-ci.org/jacebrowning/gitman
.. |Coverage Status| image:: https://coveralls.io/repos/github/jacebrowning/gitman/badge.svg?branch=develop
   :target: https://coveralls.io/github/jacebrowning/gitman?branch=develop
.. |Scrutinizer Code Quality| image:: http://img.shields.io/scrutinizer/g/jacebrowning/gitman.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/gitman/?branch=master
.. |PyPI Version| image:: http://img.shields.io/pypi/v/GitMan.svg
   :target: https://pypi.python.org/pypi/GitMan
.. |PyPI Downloads| image:: http://img.shields.io/pypi/dm/GitMan.svg
   :target: https://pypi.python.org/pypi/GitMan

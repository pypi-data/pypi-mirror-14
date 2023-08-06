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

Revision History
================

0.9 (unreleased)
----------------

- Added `edit` command to launch the configuration file.
- Depth now defaults to 5 to prevent infinite recursion.
- Fixed handling of source lists containing different dependencies.

0.8.3 (2016/03/14)
------------------

- Renamed to GitMan.

0.8.2 (2016/02/24)
------------------

- Updated to YORM v0.6.

0.8.1 (2016/01/21)
------------------

- Added an error message when attempting to lock invalid repositories.

0.8 (2016/01/13)
----------------

- Switched to using repository mirrors to speed up cloning.
- Disabled automatic fetching on install.
- Added `--fetch` option on `install` to always fetch.
- Now displaying `git status` output when there are changes.

0.7 (2015/12/22)
----------------

- Fixed `git remote rm` command (@hdnivara).
- Now applying the `update` dependency filter to locking as well.
- Now only locking previous locked dependencies.
- Added `lock` command to manually save all dependency versions.
- Now requiring `--lock` option on `update` to explicitly lock dependencies.

0.6 (2015/11/13)
----------------

- Added the ability to filter the dependency list on `install` and `update`.
- Added `--depth` option to limit dependency traversal on `install`, `update`, and `list`.

0.5 (2015/10/20)
----------------

- Added Git plugin support via: `git deps`.
- Removed `--no-clean` option (now the default) on `install` and `update`.
- Added `--clean` option to delete ignored files on `install` and `update`.
- Switched to `install` rather than `update` of nested dependencies.
- Added `--all` option on `update` to update all nested dependencies.
- Disabled warnings when running `install` without locked sources.
- Added `--no-lock` option to disable version recording.

0.4.2 (2015/10/18)
------------------

- Fixed crash when running with some sources missing.

0.4.1 (2015/09/24)
------------------

- Switched to cloning for initial working tree creation.

0.4 (2015/09/18)
----------------

- Replaced `install` command with `update`.
- Updated `install` command to use locked dependency versions.
- Now sorting sources after a successful `update`.
- Now requiring `--force` to `uninstall` with uncommitted changes.
- Updated `list` command to show full shell commands.

0.3.1 (2015/09/09)
------------------

- Ensures files are not needlessly reloaded with newer versions of YORM.

0.3 (2015/06/26)
----------------

- Added `--no-clean` option to disable removing untracked files.
- Added support for `rev-parse` dates as the dependency `rev`.

0.2.5 (2015/06/15)
------------------

- Added `--quiet` option to hide warnings.

0.2.4 (2015/05/19)
------------------

- Now hiding YORM logging bellow warnings.

0.2.3 (2015/05/17)
------------------

- Upgraded to YORM v0.4.

0.2.2 (2015/05/04)
------------------

- Specified YORM < v0.4.

0.2.1 (2015/03/12)
------------------

- Added automatic remote branch tracking in dependencies.
- Now requiring `--force` when there are untracked files.

0.2 (2015/03/10)
----------------

- Added `list` command to display current URLs/SHAs.

0.1.4 (2014/02/27)
------------------

- Fixed an outdated index when checking for changes.

0.1.3 (2014/02/27)
------------------

- Fixed extra whitespace when logging shell output.

0.1.2 (2014/02/27)
------------------

- Added `--force` argument to:
    - overwrite uncommitted changes
    - create symbolic links in place of directories
- Added live shell command output with `-vv` argument.

0.1 (2014/02/24)
----------------

- Initial release.



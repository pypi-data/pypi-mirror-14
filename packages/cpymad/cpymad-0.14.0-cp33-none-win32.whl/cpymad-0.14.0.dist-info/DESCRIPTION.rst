CPyMAD
------
|Version| |Downloads| |License| |Python|

CPyMAD is a Cython_ binding to MAD-X_.

MAD-X is a software package to simulate particle accelerators and is used
at CERN and all around the world. It has its own proprietary scripting
language and is usually launched from the command line.

This version of CPyMAD is tested with MAD-X |VERSION|. Other MAD-X
versions (and immediate revisions) might work too, but are more likely to
cause problems.

The installable wheel archives that are provided for some versions of
python to simplify the installation on windows contain a precompiled
version of CPyMAD that is statically linked against MAD-X |VERSION|.

.. _Cython: http://cython.org/
.. _MAD-X: http://cern.ch/mad
.. |VERSION| replace:: 5.02.08


Disclaimer
~~~~~~~~~~

This is a heavily modified fork of the cern-cpymad_ package. The fork is
not authored or maintained by CERN members.

CPyMAD links against an unofficial build of MAD-X that is not supported by
CERN, i.e. this binary may have problems that the official binary does not
have and vice versa. This means:

- Only report issues to CERN that can be reproduced with their official
  command line client.
- Only report issues here if they cannot be reproduced with their official
  command line client.

See `Reporting issues`_.

.. _cern-cpymad: https://github.com/pymad/cpymad


Project pages
~~~~~~~~~~~~~

- `Installation`_
- `Source code`_
- `Documentation`_
- `Issue tracker`_
- `Releases`_

.. _Installation: http://hibtc.github.io/cpymad/installation
.. _Source code: https://github.com/hibtc/cpymad
.. _Documentation: http://hibtc.github.io/cpymad
.. _Issue tracker: https://github.com/hibtc/cpymad/issues
.. _Releases: https://pypi.python.org/pypi/cpymad


Usage
~~~~~

The ``Madx`` class provides a basic binding to the MAD-X interpreter:

.. code-block:: python

    from cpymad.madx import Madx

    # Start a MAD-X interpretor. All MAD-X commands issued via cpymad will
    # be logged to `command_log`:
    madx = Madx(command_log="log.madx")

    # Show the version of MAD-X that is actually loaded:
    print(madx.version)

    # Execute one of your predefined MAD-X files:
    madx.call('/path/to/some/input_file.madx')

    # Only a handful of MAD-X methods are exposed as methods. For others,
    # you can use the `command` attribute. For example, to set a beam:
    madx.command.beam(sequence='myseq1', particle='PROTON')

    # Calculate TWISS parameters:
    twiss = madx.twiss(sequence='LEBT',
                       betx=0.1, bety=0.1,
                       alfx=0.1, alfy=0.1)

    # Your own analysis below:
    from matplotlib import pyplot as plt
    plt.plot(twiss['s'], twiss['betx'])
    plt.show()

There are alternative syntaxes for the extreme cases where you need more
fine grained control over the command string composition or where
``command`` fails to do the right thing:

.. code-block:: python

    # can't use `global` as attribute, since it's a python keyword:
    madx.command.global_(sequence='cassps', Q1=26.58)

    # can't use `: ` as attribute:
    madx.command('QP: QUADRUPOLE', AT=2, L=1)

    # issue a plain text command, don't forget the semicolon!
    madx.input('FOO, BAR=[baz], QUX=<NORF>;')


See http://hibtc.github.io/cpymad for further documentation.


Known issues
~~~~~~~~~~~~

On windows with python3.3, there is currently no satisfying way to close file
handles in the MAD-X process or prevent them from being inherited by default.
You have to make sure on your own that you close all file handles before
creating a new ``cpymad.madx.Madx`` instance!


Hacking
~~~~~~~

Try to be consistent with the PEP8_ guidelines. Add `unit tests`_ for all
non-trivial functionality. `Dependency injection`_ is a great pattern to
keep modules testable.

Commits should be reversible, independent units if possible. Use descriptive
titles and also add an explaining commit message unless the modification is
trivial. See also: `A Note About Git Commit Messages`_.

.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _`unit tests`: http://docs.python.org/2/library/unittest.html
.. _`Dependency injection`: http://www.youtube.com/watch?v=RlfLCWKxHJ0
.. _`A Note About Git Commit Messages`: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html


Reporting issues
~~~~~~~~~~~~~~~~

If you have a problem with a sequence file, first try to check if that
problem remains when using the MAD-X command line client distributed by
CERN, then:

- Report the issue to CERN only if it be reproduced with their official
  command line client.
- Report the issue here only if it cannot be reproduced with their official
  command line client.

For issues regarding the cpymad code itself or usage information, I'm happy to
answer. Just keep in mind to be **precise**, **specific**, **concise** and
provide all the necessary information.

See also:

- `Short, Self Contained, Correct (Compilable), Example`_
- `How to Report Bugs Effectively`_
- `How To Ask Questions The Smart Way`_.

.. _Short, Self Contained, Correct (Compilable), Example: http://sscce.org/
.. _How to Report Bugs Effectively: http://www.chiark.greenend.org.uk/~sgtatham/bugs.html
.. _How To Ask Questions The Smart Way: http://www.catb.org/esr/faqs/smart-questions.html


Tests
~~~~~

Currently, tests run on:

- The `Travis CI`_ service is mainly used to check that the unit tests for
  pymad itself execute on several python versions. Python{2.7,3.3} are
  supported. The tests are executed on any update of an upstream branch.
  The Travis builds use a unofficial precompiled libmadx-dev_ package to
  avoid having to rebuild the entire MAD-X library on each invocation.

  |Build| |Coverage|

.. _`Travis CI`: https://travis-ci.org/hibtc/cpymad
.. _libmadx-dev: https://github.com/hibtc/madx-debian


.. |Build| image:: https://api.travis-ci.org/hibtc/cpymad.svg?branch=master
   :target: https://travis-ci.org/hibtc/cpymad
   :alt: Build Status

.. |Coverage| image:: https://coveralls.io/repos/hibtc/cpymad/badge.svg?branch=master
   :target: https://coveralls.io/r/hibtc/cpymad
   :alt: Coverage

.. |Version| image:: http://coldfix.de:8080/v/cpymad/badge.svg
   :target: https://pypi.python.org/pypi/cpymad/
   :alt: Latest Version

.. |Downloads| image:: http://coldfix.de:8080/d/cpymad/badge.svg
   :target: https://pypi.python.org/pypi/cpymad#downloads
   :alt: Downloads

.. |License| image:: http://img.shields.io/badge/license-CC0,_Apache,_Non--Free-red.svg
   :target: https://github.com/hibtc/cpymad/blob/master/COPYING.rst
   :alt: License

.. |Python| image:: http://coldfix.de:8080/py_versions/cpymad/badge.svg
   :target: https://pypi.python.org/pypi/cpymad#downloads
   :alt: Supported Python versions

License
~~~~~~~

CPyMAD must be used in compliance with the licenses as described in the
following sections:


License for CPyMAD source
=========================

applies to the python source of the CPyMAD package::

    Copyright (c) 2013-2015, HIT - Heidelberg Ion-Therapy Center

    To the extent possible under law, the person who associated CC0 with
    CPyMAD has waived all copyright and related or neighboring rights to
    CPyMAD.

    You should have received a copy of the CC0 legalcode along with this
    work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

Note that this package is a heavily modified fork of the original
cern-cpymad package developed at CERN::

    Copyright (c) 2011, CERN. All rights reserved.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use cern-cpymad except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

For details, see the version history or ask the package maintainer.


License for MAD-X
=================

applies to binary distributions that do not require a separate
installation of MAD-X, i.e. binaries that are statically linked to MAD-X::

    CERN

    EUROPEAN ORGANISATION FOR NUCLEAR RESEARCH


    Program name:                 MAD --- Methodical Accelerator Design

    CERN program library entry:   T5001

    Authors or contacts:          mad@cern.ch
                                  BE-ABP Group
                                  CERN
                                  CH-1211 GENEVA 23
                                  SWITZERLAND


    Copyright CERN, Geneva 1990 - Copyright and any other appropriate legal
    protection of this computer program and associated documentation reserved
    in all countries of the world. Organisations collaborating with CERN may
    receive this program and documentation freely and without charge. CERN
    undertakes no obligation for the maintenance of this program, nor
    responsibility for its correctness, and accepts no liability whatsoever
    resulting from its use. Program and documentation are provided solely for
    the use of the organisation to which they are distributed. This program
    may not be copied or otherwise distributed without permission. This
    message must be retained on this and any other authorised copies. The
    material cannot be sold. CERN should be given credit in all references.

Changelog
~~~~~~~~~

(dates are in the form dd.mm.yyyy)


0.14.0
======
Date: 04.03.2016

- Add function to obtain transfer map
- Fix bug with expanded_elements listing too many elements (leading elements
  were re-listed at the end)


0.13.0
======
Date: 24.01.2016

- Update to ``MAD-X 5.02.08``:
    - official support
    - automatic tests
    - prebuilt binaries on PyPI (for windows)


0.12.2
======
Date: 30.10.2015

- Strip trailing underscore from ``MadxCommands`` attribute names. This allows
  the syntax to be used even for python keywords, e.g. ``m.command.global_()``
- Change the behaviour of ``Madx.globals``:
    - when setting string values, set the variable as deferred expression
    - when getting deferred variables, return instances of type ``Expression``
    - when iterating, only show non-constant globals


0.12.1
======
Date: 13.10.2015

- fix crash due to incorrect parameter name for ``logging.basicConfig``
- fix crash due to missing ``subprocess.MAXFD`` on python3.5
- fix coverage report submitted to coveralls.io


0.12.0
======
Date: 05.10.2015

- expose directory of global MAD-X variables as ``Madx.globals``
- expose directory of global MAD-X elements as ``Madx.elements``
- fix a bug with Elements.__contains__ reporting yes incorrectly
- list only those column of a table that are marked for output
- add function to get row names of a table


0.11.0
======
Date: 03.07.2015

- Remove models + resource handling from cpymad. If you need these, check
  them out from the previous version and maintain them in your own code
  base. This way you are much more flexible to adapt models to your needs.


0.10.8
======
Date: 02.07.2015

- Public element names are now of the form "foo[3]" or simply "foo". The
  syntax "foo:d" can not be used anymore (this form is used by MAD-X only
  internally and converted at the lowest wrapper level).
- Fix exception when not specifying sequence name on Madx methods


0.10.7
======
Date: 21.06.2015

- allow redirection of MAD-X standard I/O via Madx constructor


0.10.6
======
Date: 29.05.2015

- add csv() method for ResourceProvider
- use C loader from yaml for performance if available
- convert madx.metadata.get_copyright_notice
- add accessors to real sequence + elements for model.Sequence


0.10.5
======
Date: 25.05.2015

- add MAD-X specific metadata in cpymad.madx.metadata
- speedup Travis testing (using caches and docker containers)


0.10.4
======
Date: 22.04.2015

- prevent MAD-X process from exiting on Ctrl-C (this was an especially
  nasty feature when using the interactive python interpretor)
- upgrade to `MAD-X 5.02.05`_ (development release from 10.04.2015)
- fix leakage of open file handles into remote process on py2/windows

.. _`MAD-X 5.02.05`: http://madx.web.cern.ch/madx/releases/5.02.05/


0.10.3
======
Date: 29.03.2015

- make sequence.elements.index more convenient: can now handle names with or
  without the ':d' suffix as well as the special names '#s' and '#e'


0.10.2
======
Date: 05.03.2015

- add some utility functions to work with MAD-X element names and identifiers
- add a setter method for values to Madx
- improve install instructions. In particular, recommend WinPython as build
  environment
- fix the MinGW build error due to broken sysconfig inline
- run setup only if invoked as main script


0.10.1
======
Date: 09.01.2015

- convert IOError to RemoteProcessCrashed, which can occur on transmission
  if the remote process is already down
- convert ValueError to RemoteProcessClosed, which can occur on transmission
  if the remote process was already closed


0.10.0 Fork
===========
Date: 09.01.2015

This is the first independent version released for the `HIT cpymad fork`_.
The changes on the public API are so heavy, that this is basically a new
library.

- rename package from ``cern.cpymad`` to ``cpymad``
- remove LHC models from repository
- redesign API to make more use of OOP (no stable API yet!)
- removed some obsolete / unused modules

.. _HIT cpymad fork: https://github.com/hibtc/cpymad


0.9
===
Date: 17.11.2014

- don't link against numpy anymore (this makes distribution of prebuilt
  binaries on windows actually useful)
- add MAD-X license notice (required to distribute binaries)
- setup.py doesn't require setuptools to be pre-installed anymore (if
  internet is available)
- some doc-fixes
- convert cpymad._couch to a simple module (was a single file package)
- use ``logging`` through-out the project
- alow logger to be specified as model/madx constructor argument
- multi-column access, e.g.: ``table.columns['betx','bety']``
- move tests one folder level up


0.8
===
Date: 30.06.2014

- isolate cpymad: remove jpymad backend, remove pymad base
- bootstrap the dependency on numpy
- remove custom MAD-X path discovery during setup. You should use
  *--madxdir* if the library is not installed in a system location.
- add function ``libmadx.is_expanded``
- add function ``libmadx.chdir``
- handle MAD-X table columns with integer arrays
- make ``madx.command`` more powerful (allows ``**kwargs`` and attribute
  access)
- use inherited pipes for IPC with remote MAD-X processes (allows to
  forward stdin/stdout separately)
- close connection to remote process on finalization of ``LibMadxClient``
- remove MAD-X command checks, ``recursive_history`` and filename
  completion
- fix name clash
- fix some bugs
- rename convenience constructors to ``cern.cpymad.load_model`` and
  ``cern.cpymad.start_madx`` due to name clash with module names


0.7
===
Date: 16.04.2014

- close handles in remote process properly on all supported python versions
- rewrite ``libmadx.get_table`` functionality
- madx functions that return tables now return proxy objects instead. For
  backward compatibility these can be iterated to allow unpacking into a tuple
- the returned table columns is now a proxy object as well and not ``TfsTable``
- remove ``retdict`` parameter
- move some cpymad specific functionality into the cpymad package
- add libmadx/madx functions to access list of elements in a sequence


0.6
===
Date: 17.03.2014

- raise exception and don't hang up anymore, if libmadx process crashes
- on python>=3.4, close handles in remote process properly
- let every 'Madx' instance have an independent copy of the madx library.
  this makes the madx module much more useful. previously, this was only
  true for instances of 'cpymad.model'.
- restrict to only one cython module that links to libmadx. (allows static
  linking which is advantageous on windows!)
- use YAML model files instead of JSON
- make 'madx' a submodule of 'cpymad'
- fix test exit status


0.5
===
Date: 21.01.2014

- migrate to setuptools from distutils
- python3 support
- add continuous integration with Travis
- proper setup.py and MANIFEST.in to be used with PyPI
- rename package to 'cern-pymad'
- allow to build from PyPI without having cython



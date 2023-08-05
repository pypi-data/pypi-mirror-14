from datetime import datetime
args = ('http://pypi.python.org/pypi',)
kw = {}
data = {'package_releases':
        {('distribute',): ['0.6.15']},
        'release_data':
        {('distribute', '0.6.15'): {
            'maintainer': None,
            'requires_python': None,
            'maintainer_email': None,
            'cheesecake_code_kwalitee_id': None,
            'keywords': 'CPAN PyPI distutils eggs package management',
            'package_url': 'http://pypi.python.org/pypi/distribute',
            'author': 'The fellowship of the packaging',
            'author_email': 'distutils-sig@python.org',
            'download_url': 'UNKNOWN',
            'platform': 'UNKNOWN',
            'version': '0.6.15',
            'cheesecake_documentation_id': None,
            '_pypi_hidden': False,
            'description': """===============================
Installing and Using Distribute
===============================

.. contents:: **Table of Contents**

-----------
Disclaimers
-----------

About the fork
==============

`Distribute` is a fork of the `Setuptools` project.

Distribute is intended to replace Setuptools as the standard method
for working with Python module distributions.

The fork has two goals:

- Providing a backward compatible version to replace Setuptools
  and make all distributions that depend on Setuptools work as
  before, but with less bugs and behaviorial issues.

  This work is done in the 0.6.x series.

  Starting with version 0.6.2, Distribute supports Python 3.
  Installing and using distribute for Python 3 code works exactly
  the same as for Python 2 code, but Distribute also helps you to support
  Python 2 and Python 3 from the same source code by letting you run 2to3
  on the code as a part of the build process, by setting the keyword parameter
  ``use_2to3`` to True. See http://packages.python.org/distribute for more
  information.

- Refactoring the code, and releasing it in several distributions.
  This work is being done in the 0.7.x series but not yet released.

The roadmap is still evolving, and the page that is up-to-date is
located at : `http://packages.python.org/distribute/roadmap`.

If you install `Distribute` and want to switch back for any reason to
`Setuptools`, get to the `Uninstallation instructions`_ section.

More documentation
==================

You can get more information in the Sphinx-based documentation, located
at http://packages.python.org/distribute. This documentation includes the old
Setuptools documentation that is slowly replaced, and brand new content.

About the installation process
==============================

The `Distribute` installer modifies your installation by de-activating an
existing installation of `Setuptools` in a bootstrap process. This process
has been tested in various installation schemes and contexts but in case of a
bug during this process your Python installation might be left in a broken
state. Since all modified files and directories are copied before the
installation starts, you will be able to get back to a normal state by reading
the instructions in the `Uninstallation instructions`_ section.

In any case, it is recommended to save you `site-packages` directory before
you start the installation of `Distribute`.

-------------------------
Installation Instructions
-------------------------

Distribute is only released as a source distribution.

It can be installed using pip, and can be done so with the source tarball,
or by using the ``distribute_setup.py`` script provided online.

``distribute_setup.py`` is the simplest and preferred way on all systems.

distribute_setup.py
===================

Download
`distribute_setup.py <http://python-distribute.org/distribute_setup.py>`_
and execute it, using the Python interpreter of your choice.

If your shell has the ``curl`` program you can do::

    $ curl -O http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py

Notice this file is also provided in the source release.

pip
===

Run easy_install or pip::

    $ pip install distribute

Source installation
===================

Download the source tarball, uncompress it, then run the install command::

    $ curl -O http://pypi.python.org/packages/source/d/distribute/"""
            """distribute-0.6.15.tar.gz
    $ tar -xzvf distribute-0.6.15.tar.gz
    $ cd distribute-0.6.15
    $ python setup.py install

---------------------------
Uninstallation Instructions
---------------------------

Like other distutils-based distributions, Distribute doesn\'t provide an
uninstaller yet. It\'s all done manually! We are all waiting for PEP 376
support in Python.

Distribute is installed in three steps:

1. it gets out of the way an existing installation of Setuptools
2. it installs a `fake` setuptools installation
3. it installs distribute

Distribute can be removed like this:

- remove the ``distribute*.egg`` file located in your site-packages directory
- remove the ``setuptools.pth`` file located in you site-packages directory
- remove the easy_install script located in you ``sys.prefix/bin`` directory
- remove the ``setuptools*.egg`` directory located in your site-"""
            """packages directory,
  if any.

If you want to get back to setuptools:

- reinstall setuptools using its instruction.

Lastly:

- remove the *.OLD.* directory located in your site-packages directory if any,
  **once you have checked everything was working correctly again**.

-------------------------
Quick help for developers
-------------------------

To create an egg which is compatible with Distribute, use the same
practice as with Setuptools, e.g.::

    from setuptools import setup

    setup(...
    )

To use `pkg_resources` to access data files in the egg, you should
require the Setuptools distribution explicitly::

    from setuptools import setup

    setup(...
        install_requires=[\'setuptools\']
    )

Only if you need Distribute-specific functionality should you depend
on it explicitly. In this case, replace the Setuptools dependency::

    from setuptools import setup

    setup(...
        install_requires=[\'distribute\']
    )

-----------
Install FAQ
-----------

- **Why is Distribute wrapping my Setuptools installation?**

   Since Distribute is a fork, and since it provides the same package
   and modules, it renames the existing Setuptools egg and inserts a
   new one which merely wraps the Distribute code. This way, full
   backwards compatibility is kept for packages which rely on the
   Setuptools modules.

   At the same time, packages can meet their dependency on Setuptools
   without actually installing it (which would disable Distribute).

- **How does Distribute interact with virtualenv?**

  Everytime you create a virtualenv it will install setuptools by default.
  You either need to re-install Distribute in it right after or pass the
  ``--distribute`` option when creating it.

  Once installed, your virtualenv will use Distribute transparently.

  Although, if you have Setuptools installed in your system-wide Python,
  and if the virtualenv you are in was generated without the """
            """`--no-site-packages`
  option, the Distribute installation will stop.

  You need in this case to build a virtualenv with the `--no-site-packages`
  option or to install `Distribute` globally.

- **How does Distribute interacts with zc.buildout?**

  You can use Distribute in your zc.buildout, with the --distribute option,
  starting at zc.buildout 1.4.2::

  $ python bootstrap.py --distribute

  For previous zc.buildout versions, *the only thing* you need to do
  is use the bootstrap at `http://python-distribute.org/bootstrap.py`.  Run
  that bootstrap and ``bin/buildout`` (and all other buildout-generated
  scripts) will transparently use distribute instead of setuptools.  You do
  not need a specific buildout release.

  A shared eggs directory is no problem (since 0.6.6): the setuptools egg is
  left in place unmodified.  So other buildouts that do not yet use the new
  bootstrap continue to work just fine.  And there is no need to list
  ``distribute`` somewhere in your eggs: using the bootstrap is enough.

  The source code for the bootstrap script is located at
  `http://bitbucket.org/tarek/buildout-distribute`.



-----------------------------
Feedback and getting involved
-----------------------------

- Mailing list: http://mail.python.org/mailman/listinfo/distutils-sig
- Issue tracker: http://bitbucket.org/tarek/distribute/issues/
- Code Repository: http://bitbucket.org/tarek/distribute

=======
CHANGES
=======

------
0.6.15
------

* Fixed typo in bdist_egg
* Several issues under Python 3 has been solved.
* Issue 146: Fixed missing DLL files after easy_install of windows exe package.

------
0.6.14
------

* Issue 170: Fixed unittest failure. Thanks to Toshio.
* Issue 171: Fixed race condition in unittests cause deadlocks in test suite.
* Issue 143: Fixed a lookup issue with easy_install.
  Thanks to David and Zooko.
* Issue 174: Fixed the edit mode when its used with setuptools itself

------
0.6.13
------

* Issue 160: 2.7 gives ValueError("Invalid IPv6 URL")
* Issue 150: Fixed using ~/.local even in a --no-site-packages virtualenv
* Issue 163: scan index links before external links, and don\'t use the """
            """md5 when
  comparing two distributions

------
0.6.12
------

* Issue 149: Fixed various failures on 2.3/2.4

------
0.6.11
------

* Found another case of SandboxViolation - fixed
* Issue 15 and 48: Introduced a socket timeout of 15 seconds on url openings
* Added indexsidebar.html into MANIFEST.in
* Issue 108: Fixed TypeError with Python3.1
* Issue 121: Fixed --help install command trying to actually install.
* Issue 112: Added an os.makedirs so that Tarek\'s solution will work.
* Issue 133: Added --no-find-links to easy_install
* Added easy_install --user
* Issue 100: Fixed develop --user not taking \'.\' in PYTHONPATH into account
* Issue 134: removed spurious UserWarnings. Patch by VanLindberg
* Issue 138: cant_write_to_target error when setup_requires is used.
* Issue 147: respect the sys.dont_write_bytecode flag

------
0.6.10
------

* Reverted change made for the DistributionNotFound exception because
  zc.buildout uses the exception message to get the name of the
  distribution.

-----
0.6.9
-----

* Issue 90: unknown setuptools version can be added in the working set
* Issue 87: setupt.py doesn\'t try to convert distribute_setup.py anymore
  Initial Patch by arfrever.
* Issue 89: added a side bar with a download link to the doc.
* Issue 86: fixed missing sentence in pkg_resources doc.
* Added a nicer error message when a DistributionNotFound is raised.
* Issue 80: test_develop now works with Python 3.1
* Issue 93: upload_docs now works if there is an empty sub-directory.
* Issue 70: exec bit on non-exec files
* Issue 99: now the standalone easy_install command doesn\'t uses a
  "setup.cfg" if any exists in the working directory. It will use it
  only if triggered by ``install_requires`` from a setup.py call
  (install, develop, etc).
* Issue 101: Allowing ``os.devnull`` in Sandbox
* Issue 92: Fixed the "no eggs" found error with MacPort
  (platform.mac_ver() fails)
* Issue 103: test_get_script_header_jython_workaround not run
  anymore under py3 with C or POSIX local. Contributed by Arfrever.
* Issue 104: remvoved the assertion when the installation fails,
  with a nicer message for the end user.
* Issue 100: making sure there\'s no SandboxViolation when
  the setup script patches setuptools.

-----
0.6.8
-----

* Added "check_packages" in dist. (added in Setuptools 0.6c11)
* Fixed the DONT_PATCH_SETUPTOOLS state.

-----
0.6.7
-----

* Issue 58: Added --user support to the develop command
* Issue 11: Generated scripts now wrap their call to the script entry point
  in the standard "if name == \'main\'"
* Added the \'DONT_PATCH_SETUPTOOLS\' environment variable, so virtualenv
  can drive an installation that doesn\'t patch a global setuptools.
* Reviewed unladen-swallow specific change from
  http://code.google.com/p/unladen-swallow/source/detail?spec=svn875&r=719
  and determined that it no longer applies. Distribute should work fine with
  Unladen Swallow 2009Q3.
* Issue 21: Allow PackageIndex.open_url to gracefully handle all cases of a
  httplib.HTTPException instead of just InvalidURL and BadStatusLine.
* Removed virtual-python.py from this distribution and updated documentation
  to point to the actively maintained virtualenv instead.
* Issue 64: use_setuptools no longer rebuilds the distribute egg every
  time it is run
* use_setuptools now properly respects the requested version
* use_setuptools will no longer try to import a distribute egg for the
  wrong Python version
* Issue 74: no_fake should be True by default.
* Issue 72: avoid a bootstrapping issue with easy_install -U

-----
0.6.6
-----

* Unified the bootstrap file so it works on both py2.x and py3k without 2to3
  (patch by Holger Krekel)

-----
0.6.5
-----

* Issue 65: cli.exe and gui.exe are now generated at build time,
  depending on the platform in use.

* Issue 67: Fixed doc typo (PEP 381/382)

* Distribute no longer shadows setuptools if we require a 0.7-series
  setuptools.  And an error is raised when installing a 0.7 setuptools with
  distribute.

* When run from within buildout, no attempt is made to modify an existing
  setuptools egg, whether in a shared egg directory or a system setuptools.

* Fixed a hole in sandboxing allowing builtin file to write outside of
  the sandbox.

-----
0.6.4
-----

* Added the generation of `distribute_setup_3k.py` during the release.
  This close http://bitbucket.org/tarek/distribute/issue/52.

* Added an upload_docs command to easily upload project documentation to
  PyPI\'s http://packages.python.org.
  This close http://bitbucket.org/tarek/distribute/issue/56.

* Fixed a bootstrap bug on the use_setuptools() API.

-----
0.6.3
-----

setuptools
==========

* Fixed a bunch of calls to file() that caused crashes on Python 3.

bootstrapping
=============

* Fixed a bug in sorting that caused bootstrap to fail on Python 3.

-----
0.6.2
-----

setuptools
==========

* Added Python 3 support; see docs/python3.txt.
  This closes http://bugs.python.org/setuptools/issue39.

* Added option to run 2to3 automatically when installing on Python 3.
  This closes http://bitbucket.org/tarek/distribute/issue/31.

* Fixed invalid usage of requirement.parse, that broke develop -d.
  This closes http://bugs.python.org/setuptools/issue44.

* Fixed script launcher for 64-bit Windows.
  This closes http://bugs.python.org/setuptools/issue2.

* KeyError when compiling extensions.
  This closes http://bugs.python.org/setuptools/issue41.

bootstrapping
=============

* Fixed bootstrap not working on Windows.
  This closes http://bitbucket.org/tarek/distribute/issue/49.

* Fixed 2.6 dependencies.
  This closes http://bitbucket.org/tarek/distribute/issue/50.

* Make sure setuptools is patched when running through easy_install
  This closes http://bugs.python.org/setuptools/issue40.

-----
0.6.1
-----

setuptools
==========

* package_index.urlopen now catches BadStatusLine and malformed url errors.
  This closes http://bitbucket.org/tarek/distribute/issue/16 and
  http://bitbucket.org/tarek/distribute/issue/18.

* zip_ok is now False by default. This closes
  http://bugs.python.org/setuptools/issue33.

* Fixed invalid URL error catching. http://bugs.python.org/setuptools/issue20.

* Fixed invalid bootstraping with easy_install installation
  http://bitbucket.org/tarek/distribute/issue/40.
  Thanks to Florian Schulze for the help.

* Removed buildout/bootstrap.py. A new repository will create a specific
  bootstrap.py script.


bootstrapping
=============

* The boostrap process leave setuptools alone if detected in the system
  and --root or --prefix is provided, but is not in the same location.
  This closes http://bitbucket.org/tarek/distribute/issue/10.

---
0.6
---

setuptools
==========

* Packages required at build time where not fully present at install time.
  This closes http://bitbucket.org/tarek/distribute/issue/12.

* Protected against failures in tarfile extraction. This closes
  http://bitbucket.org/tarek/distribute/issue/10.

* Made Jython api_tests.txt doctest compatible. This closes
  http://bitbucket.org/tarek/distribute/issue/7.

* sandbox.py replaced builtin type file with builtin function open. This
  closes http://bitbucket.org/tarek/distribute/issue/6.

* Immediately close all file handles. This closes
  http://bitbucket.org/tarek/distribute/issue/3.

* Added compatibility with Subversion 1.6. This references
  http://bitbucket.org/tarek/distribute/issue/1.

pkg_resources
=============

* Avoid a call to /usr/bin/sw_vers on OSX and use the official platform API
  instead. Based on a patch from ronaldoussoren. This closes
  http://bitbucket.org/tarek/distribute/issue/5.

* Fixed a SandboxViolation for mkdir that could occur in certain cases.
  This closes http://bitbucket.org/tarek/distribute/issue/13.

* Allow to find_on_path on systems with tight permissions to fail gracefully.
  This closes http://bitbucket.org/tarek/distribute/issue/9.

* Corrected inconsistency between documentation and code of add_entry.
  This closes http://bitbucket.org/tarek/distribute/issue/8.

* Immediately close all file handles. This closes
  http://bitbucket.org/tarek/distribute/issue/3.

easy_install
============

* Immediately close all file handles. This closes
  http://bitbucket.org/tarek/distribute/issue/3.""",
            'release_url': 'http://pypi.python.org/pypi/distribute/0.6.15',
            '_pypi_ordering': 115,
            'classifiers': ['Development Status :: 5 - Production/Stable',
                            'Intended Audience :: Developers',
                            'License :: OSI Approved :: '
                            'Python Software Foundation License',
                            'License :: OSI Approved :: Zope Public License',
                            'Operating System :: OS Independent',
                            'Programming Language :: Python',
                            'Programming Language :: Python :: 3',
                            'Topic :: Software Development :: '
                            'Libraries :: Python Modules',
                            'Topic :: System :: Archiving :: Packaging',
                            'Topic :: System :: Systems Administration',
                            'Topic :: Utilities'],
            'name': 'distribute',
            'license': 'PSF or ZPL',
            'summary': 'Easily download, build, install, upgrade, and '
            'uninstall Python packages',
            'home_page': 'http://packages.python.org/distribute',
            'stable_version': None,
            'cheesecake_installability_id': None,
            },
         },
        'release_urls': {('distribute', '0.6.15'): [
            {'has_sig': False,
             'upload_time': datetime(2011, 3, 16, 16, 31, 39),
             'comment_text': '',
             'python_version': 'source',
             'url': 'http://pypi.python.org/packages/source/d/'
             'distribute/distribute-0.6.15.tar.gz',
             'md5_digest': 'ea52e1412e7ff560c290266ed400e216',
             'downloads': 0,
             'filename': 'distribute-0.6.15.tar.gz',
             'packagetype': 'sdist',
             'size': 289103}],
            }
        }

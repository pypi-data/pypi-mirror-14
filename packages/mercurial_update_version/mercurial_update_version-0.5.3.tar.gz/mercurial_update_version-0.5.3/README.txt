.. -*- mode: rst; compile-command: "rst2html README.txt README.html" -*-

=========================
Mercurial Update Version
=========================

No more manual version number editing.

Whenever you issue ``hg tag``, this extension scans your repository
for files containing various kinds of ``VERSION =`` lines, updates
those constants appropriately, commits the change, and only then tags
the release.

Functionality can be enabled per-repository or (via ``~/.hgrc``) for
many repositories at once (so you don't need to remember about
activating it on every created, or cloned repository).
|drone-badge|

.. contents::
   :local:
   :depth: 2

.. sectnum::

Enabling the extension
==========================

Install the extension as described below. Then either enable it
per-repository, or enable for many repositories at once.

Enabling per-repository
---------------------------

In repository ``.hg/hgrc`` write::

    [update_version]
    active = true
    language = python
    tagfmt = dotted

(of course using appropriate settings). Here:

- ``language`` implies version constants syntax, and sometimes
  restricts list of files scanned,

- ``tagfmt`` describes expected tag syntax (and how to extract
  actual version number from the tag).

For example, ``language = python`` means looking for ``setup.py``,
``__init__.py`` and ``version.py`` files anywhere inside the
repository, and updating lines looking like ``VERSION = "1.2.3"``,
while ``tagfmt = dotted`` means simple dotted numbers are used as
tags (``hg tag 1.0.9``).

Both languages and tag formats are configurable, extension brings
some sane defaults but they can be overridden, and new styles
can be defined. See below.

Enabling for many repositories at once
------------------------------------------------------

In ``~/.hgrc`` write something like::

    [update_version]
    pydev.active_on = ~/sources/pymodules, ~/work/python 
    pydev.language = python
    pydev.tagfmt = dotted
    myperl.active_on = ~/scripts, ~/work/scripts 
    myperl.language = perl
    myperl.tagfmt = dashed

Key prefixes (``pydev`` and ``myperl``) are used only to group
three settings together (use any names you like).

In both cases:

- ``.active_on`` lists directory trees to which given rule can be applied
  (absolute paths, ``~`` and ``~user`` are allowed), 

- ``.language`` and ``.tagfmt`` define which language settings and which tag
  format to use for those directories.

Using
============================================

After enabling the extension:

- ensure your code have some initial version variables
  (put sth. like ``VERSION = "0.0.0"`` in appropriate place(s))

- simply ``hg tag «appropriate-tag»``.

Version numbers are not updated when tag is placed by revision (``hg
tag -r «version-no» «tag»``), unless specified revision matches
currently checked out revision.

Tags not matching the pattern and local tags (rarely used Mercurial
feature) are also ignored.

The extension notifies you whether and what it does, for example::

  $ hg tag 2.0
  update_version: Version number in src/version.py set to 2.0. List of changes:
      Line 2
      < VERSION = "1.0"
      > VERSION = "2.0"

or::

  $ hg tag -r 2 0.5.0
  update_version: ignoring tag placed -r revision (tag is placed, but version number not updated)

Predefined languages
=============================================

The ``language`` setting defines:

- which files to check and patch (by filename patterns)

- what is the appropriate constant format and name

The following languages are currently supported:

``python``
    Look for files named ``setup.py``, ``__init__.py`` or
    ``version.py`` (anywhere inside repository). In those files,
    update lines looking like::

        VERSION = '1.2.3'

    (at least one dot - but can be more, both single and double-quotes
    are supported, just like various spacing and indentation).
    
    Inserted version number is formatted in the same way (as
    dot-separated list of numbers).  Tag being placed should contain
    at least two-part version number to be used.

``perl``
    Look for files named ``*.pl``, ``*.pm`` and ``*.pod`` around
    repository. If found, look for lines like::

        our $VERSION = '1.00';
        my $VERSION = '11.72';
        use constant VERSION => '21.3374';

    (exactly one dot expected, various spacing and indentation
    allowed, double quotes allowed) and also::

        Version 1.23

    (usually met in POD sections).

    Also, look for ``dist.ini`` and if found, fix lines like::

        version = 0.02

    Two kinds of tags numbers are supported. If tag contains two-item
    version, it is left as is (tag ``1.0`` results in version ``1.0``,
    dashed tag ``1-03`` brings ``1.03``). If tag has three parts,
    first is left before the dot while second and third each get two
    digits after the dot (tag ``1.7.2`` is translated into version
    ``1.0702``, tag ``17-0-9`` into ``17.0009``). Other tags are
    invalid.

*Support for further languages is planned, feel free to suggest them.*

Predefined tag formats
=============================

``dotted``
    Tags like ``1.0``, ``1.0.3``, ``11.17.34``.

``dashed``
    Tags like ``1-0``, ``1-0-3``, ``11-17-34``.
    
``pfx-dotted``
    Tags like ``mylib-1.0`` or ``sth_11.3.17``:
    alphanumeric string, dash or underscore,
    then actual version as in ``dotted``.

``pfx-dashed``
    Tags like ``mylib-1-0`` or ``sth_11-3-17``:
    alphanumeric string, dash or underscore,
    then actual version as in ``dashed``. leading
    part must not end with digit.

Custom languages
=============================

Not yet supported, but planned (defining new language by configuration
settings, or overriding some default language characteristics). The
general idea is to have some reasonable defaults built-in, but allow
reconfiguration.


Custom tag formats
=============================

Not yet supported, but planned (defining new tag format by
configuration settings).


Commands
=====================

Extension mainly work by augmenting ``hg tag``. The command::

    hg tag_version_test 1.0

does *dry-run* check – lists which files would be checked, whether
version lines were found in them, and how would they be fixed.


Installation
==================

Linux/Unix (from PyPI)
---------------------------------------------

If you have working ``pip`` or ``easy_install``::

    pip install --user mercurial_update_version

or maybe::

    sudo pip install mercurial_update_version

(or use ``easy_install`` instead of ``pip``). Then activate by::

    [extensions]
    mercurial_update_version =

To upgrade, repeat the same command with ``--upgrade`` option, for
example::

    pip install --user --upgrade mercurial_update_version

Linux/Unix (from source)
---------------------------------------------

If you don't have ``pip``, or wish to follow development more closely:

- clone both this repository and `mercurial_extension_utils`_ and put
  them in the same directory, for example::

    cd ~/sources
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/
    hg clone https://bitbucket.org/Mekk/mercurial-update_version/

- update to newest tags,

- activate by::

    [extensions]
    mercurial_update_version = ~/sources/mercurial-update_version/mercurial_update_version.py

To upgrade, pull and update.

See `mercurial_extension_utils`_ for longer description of this kind
of installation.

Windows
---------------------------------------------

If you have any Python installed, you may install with ``pip``::

    pip install mercurial_update_version

Still, as Mercurial (whether taken from TortoiseHg_, or own package)
uses it's own bundled Python, you must activate by specifying the path::

    [extensions]
    mercurial_update_version = C:/Python27/Lib/site-packages/mercurial_update_version.py
    ;; Or wherever pip installed it

To upgrade to new version::

    pip --upgrade mercurial_update_version

If you don't have any Python, clone repositories::

    cd c:\hgplugins
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/
    hg clone https://bitbucket.org/Mekk/mercurial-update_version/

update to tagged versions and activate by path::

    [extensions]
    mercurial_update_version = C:/hgplugins/mercurial-update_version/mercurial_update_version.py
    ;; Or wherever you cloned

See `mercurial_extension_utils`_ documentation for more details on
Windows installation. 


History
==================================================

See `HISTORY.txt`_


Development, bug reports, enhancement suggestions
===================================================

Development is tracked on BitBucket, see 
http://bitbucket.org/Mekk/mercurial-update_version/

Use BitBucket issue tracker for bug reports and enhancement
suggestions.

Additional notes
================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/UpdateVersionExtension

Check also `other Mercurial extensions I wrote`_.

.. _other Mercurial extensions I wrote: http://mekk.bitbucket.org/mercurial.html

.. _Mercurial: http://mercurial.selenic.com
.. _HISTORY.txt: http://bitbucket.org/Mekk/mercurial-update_version/src/tip/HISTORY.txt
.. _mercurial_extension_utils: https://bitbucket.org/Mekk/mercurial-extension_utils/
.. _TortoiseHg: http://tortoisehg.bitbucket.org/

.. |drone-badge| 
    image:: https://drone.io/bitbucket.org/Mekk/mercurial-update_version/status.png
     :target: https://drone.io/bitbucket.org/Mekk/mercurial-update_version/latest
     :align: middle

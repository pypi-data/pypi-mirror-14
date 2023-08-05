.. -*- mode: rst; compile-command: "rst2html README.txt README.html" -*-

====================================
Mercurial All Dirs extension
====================================

Execute the same Mercurial command in many repositories.
|drone-badge|

.. contents::
   :local:
   :depth: 2

.. sectnum::

Example
=====================

Imagine you have Mercurial repositories in ``~/src/libs/acme``, 
``~/src/libs/net/aaa``, and ``~/src/libs/net/bbb``. Then::

    cd ~/src/libs
    hg alldirs status
    # … shows status in all three repos
    hg alldirs heads -t
    # … and heads
    hg alldirs log -l 2
    # … and recent commit

and even::

    hg alldirs commit -m "Documentation updates"
    # Commit in all three repos
    hg alldirs push bb
    # … and pushes them all

Relative file names are resolved against given repo root (the
command chdirs to every repo before actually executing it)::

    hg alldirs commit -m "Version update" setup.py src/version.py 

.. note::

   In practice I usually shortcut the command and type::

        hg alld status
        # etc

Note that ``alldirs`` does not require any kind of *parent
repository*.

In case you are already inside some repo, command is executed on
it, so ``alld`` does not matter::

    cd ~/src/libs/net/aaa
    hg status
    hg alld status
    # … Both do the same


Failure handling
=================================================

In case given command is not known (``hg alldirs badcommand``), or
got invalid options (``hg alldirs log -s``), error is reported
immediately and processing stops.

.. note::

   Technically: command name and params are parsed once, before
   visiting subdirs.

In case given commands fails during execution (``hg alldirs pull
nosuchalias``), ``alldirs`` executes the command in every repo
(doesn't stop). After finishing the job, it summarizes list of
repositories in which th ecommand failed.

.. note::

   That is done on purpose, I do not want my ``hg alld pull``
   to break if some repo lacks default path.

In both cases whole command returns exit status signalling
an error. 


Installation
=================================================

Linux/Unix (from PyPI)
~~~~~~~~~~~~~~~~~~~~~~

If you have working ``pip`` or ``easy_install``::

    pip install --user mercurial_all_dirs

or maybe::

    sudo pip install mercurial_all_dirs

(or use ``easy_install`` instead of ``pip``). Then activate by::

    [extensions]
    mercurial_all_dirs =

To upgrade, repeat the same command with ``--upgrade`` option, for
example::

    pip install --user --upgrade mercurial_all_dirs

Linux/Unix (from source)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't have ``pip``, or wish to follow development more closely:

- clone both this repository and `mercurial_extension_utils`_ and put
  them in the same directory, for example::

    cd ~/sources
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/
    hg clone https://bitbucket.org/Mekk/mercurial-all_dirs/

- update to newest tags,

- activate by::

    [extensions]
    mercurial_all_dirs = ~/sources/mercurial-all_dirs/mercurial_all_dirs.py

To upgrade, pull and update.

See `mercurial_extension_utils`_ for longer description of this kind
of installation.

Windows
~~~~~~~~~~~~~~~~~~~~~~~

If you have any Python installed, you may install with ``pip``::

    pip install mercurial_all_dirs

Still, as Mercurial (whether taken from TortoiseHg_, or own package)
uses it's own bundled Python, you must activate by specifying the path::

    [extensions]
    mercurial_all_dirs = C:/Python27/Lib/site-packages/mercurial_all_dirs.py
    ;; Or wherever pip installed it

To upgrade to new version::

    pip --upgrade mercurial_all_dirs

If you don't have any Python, clone repositories::

    cd c:\hgplugins
    hg clone https://bitbucket.org/Mekk/mercurial-extension_utils/
    hg clone https://bitbucket.org/Mekk/mercurial-all_dirs/

update to tagged versions and activate by path::

    [extensions]
    mercurial_all_dirs = C:/hgplugins/mercurial-all_dirs/mercurial_all_dirs.py
    ;; Or wherever you cloned

See `mercurial_extension_utils`_ documentation for more details on
Windows installation. 



Related extensions
==================================================

There are a few extensions which support operations on repository
groups - `Subrepos Extension`_, `OnSub Extension`_, `Forest
Extension`_. They all require using parent repository, which defines
the project structure. So, to pull all repos below ``~/src`` you
must ``hg init src``, create file like ``.hgsub`` there, etc.

All Dirs does not require such a parent repo. It just works on
whatever is found on the disk. You decided to keep some repositories
below ``~/src``? Fine, you can ``hg alld status`` them all.

Command syntax also matters. I strongly prefer typing::

     hg alld pull --update

to typing::

     hg onsub "hg pull --update"

At the same time, All Dirs does not support any kind of declaration
that some repositories are related, group cloning, version
relationship etc. If you are interested in such features, consider
`Subrepos Extension`_.

History
==================================================

See `HISTORY.txt`_

Development, bug reports, enhancement suggestions
===================================================

Development is tracked on BitBucket, see 
http://bitbucket.org/Mekk/mercurial-all_dirs/

Use BitBucket issue tracker for bug reports and enhancement
suggestions.

Additional notes
================

Information about this extension is also available
on Mercurial Wiki: http://mercurial.selenic.com/wiki/AllDirsExtension

Check also `other Mercurial extensions I wrote`_.

.. _other Mercurial extensions I wrote: http://mekk.bitbucket.org/mercurial.html

.. _Mercurial: http://mercurial.selenic.com
.. _HISTORY.txt: http://bitbucket.org/Mekk/mercurial-all-dirs/src/tip/HISTORY.txt
.. _mercurial_extension_utils: https://bitbucket.org/Mekk/mercurial-extension_utils/
.. _dynamic_username: http://bitbucket.org/Mekk/mercurial-dynamic_username/

.. _TortoiseHg: http://tortoisehg.bitbucket.org/

.. _OnSub Extension: https://www.mercurial-scm.org/wiki/OnsubExtension
.. _Subrepos Extension: https://www.mercurial-scm.org/wiki/Subrepository
.. _Forest Extension: https://www.mercurial-scm.org/wiki/ForestExtension

.. |drone-badge| 
    image:: https://drone.io/bitbucket.org/Mekk/mercurial-all_dirs/status.png
     :target: https://drone.io/bitbucket.org/Mekk/mercurial-all_dirs/latest
     :align: middle

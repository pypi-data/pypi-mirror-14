.. -*- mode: rst; coding: utf-8 -*-

=======================================================
mekk.fics
=======================================================

``mekk.fics`` is a Python access library for FICS_.
It can be used to write FICS bots and clients in Python.
|drone-badge|

Status
=======================================================

The code works, and is actively used, but covers only part of FICS
functionality.

Core functionality (handling FICS connections, command management etc)
works, is stable and have been used by WatchBot_ for many years.

Parsing routines (converting various FICS notifications and replies to
commands) are implemented only for some commands and notifications.
New parsers are mostly added on demand, whenever some new command or
information turns out to be useful.

Main APIs should be stable, data structures can be modified from time
to time.

Examples and documentation
=======================================================

In case you are not familiar with FICS programming, take a look at:

   `How to write a FICS bot`_

article series.

Next please take a look at `mekk.fics examples`_. 

All important classes and methods have docstrings.

Development
=======================================================

The code is tracked using Mercurial. Repository can be cloned from

    `http://bitbucket.org/Mekk/mekk.fics`_

Use the same place to report bugs, suggest improvements and offer
patches.

Installation
=======================================================

From PyPI (installing newest release)::

    pip install --user mekk.fics

from source (tagged release)::

    hg clone http://bitbucket.org/Mekk/mekk.fics
    hg update -r 'max(tagged())'
    pip install --user .

from source, for development::
    
    hg clone http://bitbucket.org/Mekk/mekk.fics
    pip install --user --edit .


License
=======================================================

mekk.fics is dual-licensed under Artistic License 2.0 and Mozilla Public
License 1.1. The complete license texts can be found in Artistic-2.0.txt
and MPL-1.1.txt.

.. _FICS: http://www.freechess.org
.. _WatchBot: http://mekk.waw.pl/mk/watchbot/index
.. _How to write a FICS bot: http://blog.mekk.waw.pl/series/how_to_write_fics_bot/index.html
.. _mekk.fics examples: https://bitbucket.org/Mekk/mekk.fics/src/tip/sample
.. _http://bitbucket.org/Mekk/mekk.fics: http://bitbucket.org/Mekk/mekk.fics

.. |drone-badge| 
    image:: https://drone.io/bitbucket.org/Mekk/mekk.fics/status.png
     :target: https://drone.io/bitbucket.org/Mekk/mekk.fics/latest
     :align: middle

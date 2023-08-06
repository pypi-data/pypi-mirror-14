.. This file is a part of the AnyBlok / Pyramid / Beaker project
..
..    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

Front Matter
============

Information about the AnyBlok / Pyramid / Beaker project.

Project Homepage
----------------

AnyBlok is hosted on `Bitbucket <http://bitbucket.org>`_ - the main project
page is at https://bitbucket.org/jssuzanne/anyblok_pyramid_beaker. Source code is
tracked here using `Mercurial <http://mercurial.selenic.com>`_.

Releases and project status are available on Pypi at
http://pypi.python.org/pypi/anyblok_pyramid_beaker.

The most recent published version of this documentation should be at
http://doc.pyramid.anyblok.org.

Project Status
--------------

AnyBlok with Pyramid is currently in beta status and is expected to be fairly
stable.   Users should take care to report bugs and missing features on an as-needed
basis.  It should be expected that the development version may be required
for proper implementation of recently repaired issues in between releases;
the latest master is always available at http://bitbucket.org/jssuzanne/anyblok_pyramid_beaker/get/default.tar.gz.

Installation
------------

Install released versions of AnyBlok from the Python package index with
`pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::

    pip install anyblok_pyramid_beaker

Installation via source distribution is via the ``setup.py`` script::

    python setup.py install

Installation will add the ``anyblok``and ``anyblok_pyramid`` commands to the environment.

Unit Test
---------

Run the test with ``nose``::

    pip install nose
    nosetests anyblok_pyramid_beaker/tests

Dependencies
------------

AnyBlok works with **Python 3.3** and later. The install process will
ensure that `AnyBlok <http://doc.anyblok.org>`_,
`AnyBlok / Pyramid <http://docs.anybox.fr/anyblok_pyramid/default>`_ 
are installed, in addition to other dependencies. The latest version of them 
is strongly recommended.


Contributing (hackers needed!)
------------------------------

Anyblok / Pyramid / Beaker is at a very early stage, feel free to fork, talk 
with core dev, and spread the word!

Author
------

Jean-Sébastien Suzanne

Contributors
------------

`Anybox <http://anybox.fr>`_ team:

* Jean-Sébastien Suzanne

Bugs
----

Bugs and feature enhancements to AnyBlok should be reported on the `Issue
tracker <https://bitbucket.org/jssuzanne/anyblok_pyramid_beaker/issues>`_.

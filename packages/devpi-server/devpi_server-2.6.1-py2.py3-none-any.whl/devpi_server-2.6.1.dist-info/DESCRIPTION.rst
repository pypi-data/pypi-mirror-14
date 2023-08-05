devpi-server: consistent pypi.python.org cache, github-style internal indexes
=============================================================================

* `issue tracker <https://bitbucket.org/hpk42/devpi/issues>`_, `repo
  <https://bitbucket.org/hpk42/devpi>`_

* IRC: #devpi on freenode, `mailing list
  <https://groups.google.com/d/forum/devpi-dev>`_ 

* compatibility: {win,unix}-py{26,27,34}

consistent robust pypi-cache
----------------------------------------

You can point ``pip or easy_install`` to the ``root/pypi/+simple/``
index, serving as a self-updating transparent cache for pypi-hosted
**and** external packages.  Cache-invalidation uses the latest and
greatest PyPI protocols.  The cache index continues to serve when
offline and will resume cache-updates once network is available.

github-style indexes
---------------------------------

Each user can have multiple indexes and upload packages and docs via
standard ``setup.py`` invocations.  Users, indexes (and soon projects
and releases) are manipulaed through a RESTful HTTP API.

index inheritance
--------------------------

Each index can be configured to merge in other indexes so that it serves
both its uploads and all releases from other index(es).  For example, an
index using ``root/pypi`` as a parent is a good place to test out a
release candidate before you push it to PyPI.

good defaults and easy deployment
---------------------------------------

Get started easily and create a permanent devpi-server deployment
including pre-configured templates for ``nginx`` and cron. 

separate tool for Packaging/Testing activities
-------------------------------------------------------

The complimentary `devpi-client <http://pypi.python.org/devpi-client>`_ tool
helps to manage users, indexes, logins and typical setup.py-based upload and
installation workflows.

See http://doc.devpi.net for getting started and documentation.



Changelog
=========

2.6.1 (2016-03-03)
------------------

- add more info when importing data.  Thanks Marc Abramowitz for the PR.

- include version in file paths in exported data to avoid possible
  name conflicts.


2.6.0 (2016-01-29)
------------------

- fix issue262: new experimental option --offline-mode will prevent
  devpi-server from even trying to perform network requests and it
  also strip all non-local release files from the simple index.
  Thanks Daniel Panteleit for the PR.

- fix issue304: mark devpi-server versions older than 2.2.x as incompatible
  and requiring an import/export cycle.

- fix issue296: try to fetch files from master again when requested, if there
  were checksum errors during replication.

- if a user can't be found during authentication (with ``setup.py upload`` for
  example), then the http return code is now 401 instead of 404.

- fix issue293: push from root/pypi to another index is now supported

- fix issue265: ignore HTTP(S) proxies when checking if the server is
                already running.

- Add ``content_type`` route predicate for use by plugins.


2.5.3 (2015-11-23)
------------------

- fix a bug that resulted from accessing a non-existing project on 
  root/pypi where upstream does not contain the X-PYPI-LAST-SERIAL
  header usually.  Thanks Matthias Bach.


2.5.2 (2015-11-20)
------------------

- recognize "pex" for redirections of user/index/NAME to
  user/index/+simple/NAME just like we do with pip/setuptools.

- fix py2 incompatibility introduced with 2.5.1 where we used
  a unicode header and pyramid only likes str-headers.


2.5.1 (2015-11-20)
------------------

- fix issue289: fix simple page serving on replicas




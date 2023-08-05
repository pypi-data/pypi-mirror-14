PyPI Cloud
==========
:Build: |build|_ |coverage|_
:Documentation: http://pypicloud.readthedocs.org/
:Downloads: http://pypi.python.org/pypi/pypicloud
:Source: https://github.com/mathcamp/pypicloud

.. |build| image:: https://travis-ci.org/mathcamp/pypicloud.png?branch=master
.. _build: https://travis-ci.org/mathcamp/pypicloud
.. |coverage| image:: https://coveralls.io/repos/mathcamp/pypicloud/badge.png?branch=master
.. _coverage: https://coveralls.io/r/mathcamp/pypicloud?branch=master

This package is a Pyramid app that runs a simple PyPI server where all the
packages are stored on Amazon's Simple Storage Service (S3).

`LIVE DEMO <http://pypi.stevearc.com>`_

Quick Start
===========
For more detailed step-by-step instructions, check out the `getting started
<http://pypicloud.readthedocs.org/en/latest/topics/getting_started.html>`_
section of the docs.

::

    virtualenv mypypi
    source mypypi/bin/activate
    pip install pypicloud[server]
    pypicloud-make-config -t server.ini
    pserve server.ini

It's running! Go to http://localhost:6543/ to view the web interface.

Docker
------
There is a docker image if you're into that sort of thing. You can find it at:
https://github.com/stevearc/pypicloud-docker


Changelog
=========
If you are upgrading an existing installation, read the instructions

0.3.10
------
* Feature: S3 backend setting ``storage.redirect_urls``

0.3.9
-----
* Bug fix: SQL cache works with MySQL 
* Feature: S3 backend can use S3-compatible APIs 

0.3.8
-----
* Feature: Cloudfront storage 
* Bug fix: Rebuilding cache from storage won't crash on odd file names 

0.3.7
-----
* Feature: ``/packages`` endpoint to list all files for all packages 

0.3.6
-----
* Bug fix: Settings parsed incorrectly for LDAP auth 

0.3.5
-----
* Bug fix: Mirror mode: only one package per version is displayed 

0.3.4
-----
* Add docker-specific option for config creation
* Move docker config files to a separate repository

0.3.3
-----
* Feature: LDAP Support 
* Bug fix: Incorrect package name/version when uploading from web 

0.3.2
-----
* Bug fix: Restore direct links to S3 to fix easy_install 

0.3.1
-----
* Bug fix: ``pypi.allow_overwrite`` causes crash in sql cache 

0.3.0
-----
* Fully defines the behavior of every possible type of pip request. See Fallbacks for more detail.
* Don't bother caching generated S3 urls.

0.2.13
------
* Bug fix: Crash when mirror mode serves private packages

0.2.12
------
* Bug fix: Mirror mode works properly with S3 storage backend

0.2.11
------
* Bug fix: Cache mode will correctly download packages with legacy versioning 
* Bug fix: Fix the fetch_requirements endpoint 
* Bug fix: Incorrect expire time comparison with IAM roles 
* Feature: 'mirror' mode. Caches packages, but lists all available upstream versions.

0.2.10
------
* Bug fix: S3 download links expire incorrectly with IAM roles 
* Bug fix: ``fallback = cache`` crashes with distlib 0.2.0 

0.2.9
-----
* Bug fix: Connection problems with new S3 regions 
* Usability: Warn users trying to log in over http when ``session.secure = true`` 

0.2.8
-----
* Bug fix: Crash when migrating packages from file storage to S3 storage 

0.2.7
-----
* Bug fix: First download of package using S3 backend and ``pypi.fallback = cache`` returns 404 

0.2.6
-----
* Bug fix: Rebuilding SQL cache sometimes crashes 

0.2.5
-----
* Bug fix: Rebuilding SQL cache sometimes deadlocks 

0.2.4
-----
* Bug fix: ``ppc-migrate`` between two S3 backends 

0.2.3
-----
* Bug fix: Caching works with S3 backend 

0.2.2
-----
* Bug fix: Security bug in user auth 
* Bug fix: Package caching from pypi was slightly broken 
* Bug fix: ``ppc-migrate`` works when migrating to the same storage type 

0.2.1
-----
* Bug fix: Pre-existing S3 download links were broken by 0.2.0 

0.2.0
-----
**Upgrade breaks**: caching database

* Bug fix: Timestamp display on web interface 
* Bug fix: User registration stores password as plaintext 
* Feature: ``ppc-migrate``, command to move packages between storage backends 
* Feature: Adding support for more than one package with the same version. Now you can upload wheels! 
* Feature: Allow transparently downloading and caching packages from pypi 
* Feature: Export/Import access-control data via ``ppc-export`` and ``ppc-import`` 
* Feature: Can set default read/write permissions for packages 
* Feature: New cache backend: DynamoDB 
* Hosting all js & css ourselves (no more CDN links) 
* Obligatory miscellaneous refactoring

0.1.0
-----
* First public release



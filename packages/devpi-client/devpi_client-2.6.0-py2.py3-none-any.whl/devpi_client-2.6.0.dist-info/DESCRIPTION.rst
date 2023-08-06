devpi-client: commands for python packaging and testing
===============================================================

The "devpi" command line tool is typically used in conjunction
with `devpi-server <http://pypi.python.org/pypi/devpi-server>`_.
It allows to upload, test and install packages from devpi indexes.
See http://doc.devpi.net for quickstart and more documentation.

* `issue tracker <https://bitbucket.org/hpk42/devpi/issues>`_, `repo
  <https://bitbucket.org/hpk42/devpi>`_

* IRC: #devpi on freenode, `mailing list
  <https://groups.google.com/d/forum/devpi-dev>`_ 

* compatibility: {win,unix}-py{26,27,33}





Changelog
=========

2.6.0 (2016-04-22)
------------------

- switching to another server with ``devpi use`` now reuses an existing
  authentication token as well as previously set basic auth and client cert.

- basic authentication is now stored at the devpi-server root instead of the
  domain root, so you can have more than one devpi-server on different paths
  with different basic auth.

- fix issue318: ``devpi test --index`` now accepts a URL, so one can test a
  package from another server without having to run ``devpi use`` first.


2.5.0 (2016-02-08)
------------------

- the ``user`` command now behaves slightly more like ``index`` to show
  current user settings and modify them.

- fix issue309: print server versions with ``devpi --version`` if available.
  This is only supported on Python 3.x because of shortcomings in older
  argparse versions for Python 2.x.

- fix issue310: with --set-cfg the ``index`` setting in the ``[search]``
  section would be set multiple times.

- fix getjson to work when no index but a server is selected

- allow full urls for getjson

- "devpi quickstart" is not documented anymore and will be removed
  in a later release.


2.4.1 (2016-02-01)
------------------

- fix issue308: properly handle index reconfiguration in the client API.
  thanks to Jacob Geiger for the report and an initial PR.


2.4.0 (2016-01-29)
------------------

- fix issue291: transfer file modes with vcs exports.  Thanks Sergey
  Vasilyev for the report.

- new option "--index" for "install", "list", "push", "remove", "upload" and
  "test" which allows to use a different than the current index without using
  "devpi use" before

- set ``index`` in ``[search]`` section of ``pip.cfg`` when writing cfgs, to
  support ``pip search``


2.3.2 (2015-11-11)
------------------

- fix git submodules for devpi upload. ``.git`` is a file not a folder for
  submodules. Before this fix the repository which contains the submodule was
  found instead, which caused a failure, because the files aren't tracked there.

- new option "devpi upload --setupdir-only" which will only
  vcs-export the directory containing setup.py. You can also
  set "setupdirs-only = 1" in the "[devpi:upload]" section
  of setup.cfg for the same effect.  Thanks Chad Wagner for the PR.




tox-run-command
===============

A tox plugin to run an arbitrary command in a tox managed virtualenv.

Example:
  ``tox -e py27 --run-command "server --port 8080"``

In the example tox will will run ``server --port 8080`` inside of the py27
virualenv.

Notes:

* Any env defined in your tox.ini will work
* The env will be created if it doesn't exist (just like tox normally
  does)
* The commands from your tox.ini will not be run and instead the command
  you wanted to run is run
* `tox substitutions`_ will also work.
  (e.g. ``tox -e py27 --run-command "server --config={homedir}/server.conf"``)

Why?
----

Almost all of the projects I work on use `tox`_ for test automation. Many
of those projects, one such example is `Keystone`_, carry custom Python
and/or shell scripts to create virtualenvs to run server processes for
manual testing. Other projects advise the developer to create a tox
virtualenv by running ``tox -e py27 --notest`` and then running the
server from within that virtualenv like ``.tox/py27/bin/server --port
8080``.

Both of those options suck. Since I couldn't find a tool that already existed
to do this, I created one using the new `tox plugin API`_.

.. _tox: https://testrun.org/tox/latest/
.. _Keystone: http://docs.openstack.org/developer/keystone/
.. _tox plugin API: https://testrun.org/tox/latest/plugins.html
.. _tox substitutions: https://testrun.org/tox/latest/config.html#substitutions

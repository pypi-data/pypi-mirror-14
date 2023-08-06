=====
janus
=====

Python client for `Janus <https://github.com/meetecho/janus-gateway>`_.

dev
---

Setup a `venv <https://virtualenvwrapper.readthedocs.org/en/latest/>`_:

.. code:: bash

   $ mkvirtualenv janus
   (janus)$ pip install -e .[test]

and test it:

.. code:: bash

   (janus)$ py.test test/ --cov janus --cov-report term-missing --pep8

usage
-----

Typical usage is to create a representation of your Janus `Plugin`:

.. code:: python

    class MyPlugin(janus.Plugin):

        name = 'janus.plugin.krazyeyezkilla'

        def sup(self, greets)
            self.send_message({'wat': greets})


    my_plugin = MyPlugin()

setup a `Session`:

.. code:: python

    session = janus.Session('ws://127.0.0.1', secret='janusrocks')
    session.register_plugin(my_plugin)

keep it alive:

.. code:: python

    session_ka = janus.KeepAlive(session)
    session_ka.daemon = True
    session_ka.start()

and then use your plugin:

.. code:: python

    my_plugin.sup('dawg')

release
-------

Tests pass:

.. code:: bash

   py.test test/ --cov janus --cov-report term-missing --pep8

so update ``__version__`` in ``janus.py``. Commit and tag it:

.. code:: bash

   git commit -am "release v{version}"
   git tag -a v{version} -m "release v{version}"
   git push --tags

and `travis <https://travis-ci.org/mayfieldrobotics/janus>`_ will publish it to `pypi <https://pypi.python.org/pypi/janus/>`_.

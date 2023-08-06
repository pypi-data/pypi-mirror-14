airbrake-python
===============

`Airbrake <https://airbrake.io/>`__ integration for python that quickly
and easily plugs into your existing code.

.. code:: python

    import airbrake

    logger = airbrake.getLogger()

    try:
        1/0
    except Exception:
        logger.exception("Bad math.")

airbrake-python is used most effectively through its
`logging <http://docs.python.org/2/library/logging.html>`__ handler, and
uses the `Airbrake V3
API <https://help.airbrake.io/kb/api-2/notifier-api-v3>`__ for error
reporting.

install
~~~~~~~

To install airbrake-python, run:

.. code:: bash

    $ pip install -U airbrake

setup
~~~~~

The easiest way to get set up is with a few environment variables:

.. code:: bash

    export AIRBRAKE_API_KEY=*****
    export AIRBRAKE_PROJECT_ID=12345
    export AIRBRAKE_ENVIRONMENT=dev

and you're done!

Otherwise, you can instantiate your ``AirbrakeHandler`` by passing these
values as arguments to the ``getLogger()`` helper:

.. code:: python

    import airbrake

    logger = airbrake.getLogger(api_key=*****, project_id=12345)

    try:
        1/0
    except Exception:
        logger.exception("Bad math.")

setup for Airbrake On-Premise and other compatible back-ends (e.g. Errbit)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Airbrake `Enterprise <https://airbrake.io/enterprise>`__ and self-hosted
alternatives, such as `Errbit <https://github.com/errbit/errbit>`__,
provide a compatible API.

You can configure a different endpoint than the default
(``https://airbrake.io``) by either:

-  Setting an environment variable:

.. code:: bash

    export AIRBRAKE_BASE_URL=https://self-hosted.errbit.example.com/

-  Or passing a ``base_url`` argument to the ``getLogger()`` helper:

.. code:: python

    import airbrake

    logger = airbrake.getLogger(api_key=*****, project_id=12345, base_url="https://self-hosted.errbit.example.com/")

adding the AirbrakeHandler to your existing logger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import logging

    import airbrake

    yourlogger = logging.getLogger(__name__)
    yourlogger.addHandler(airbrake.AirbrakeHandler())

*by default, the ``AirbrakeHandler`` only handles logs level ERROR (40)
and above*

giving your exceptions more context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import airbrake

    logger = airbrake.getLogger()

    def bake(**goods):
        try:
            temp = goods['temperature']
        except KeyError as exc:
            logger.error("No temperature defined!", extra=goods)

--------------

| The `airbrake.io <https://airbrake.io/>`__ docs used to implement
  airbrake-python are here:
| http://help.airbrake.io/kb/api-2/notifier-api-v3

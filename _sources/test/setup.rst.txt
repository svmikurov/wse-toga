==========
Test setup
==========

Setup
=====

How to run tests see
`BeeWare Tutorial <https://docs.beeware.org/en/latest/tutorial/topics/testing.html#testing-times>`_:

"We can run this test suite using the ``--test`` option to briefcase dev.
As this is the first time we are running tests, we also need to pass
in the ``-r`` option to ensure that the test requirements are also installed:
``briefcase dev --test -r``."

Make sure application dependencies are updated, see
`Updating dependencies <https://docs.beeware.org/en/latest/tutorial/tutorial-7.html#updating-dependencies>`_.

To test Toga widgets install
`toga-dummy <https://toga.readthedocs.io/en/latest/reference/platforms/testing.html#testing>`_.

Add to ``pyproject.toml``::

    requires = [
        ...,
        # https://pypi.org/project/toga-dummy/
        "toga-dummy==0.4.8 ",
        ...,
    ]

Add to ``Makefile``::

    test:
        export TOGA_BACKEND=toga_dummy && \
        briefcase dev --test

Run tests::

    make test

Fixtures
========

``conftest.py``::

    import asyncio

    import pytest

    import toga

    from wse.app import WSE

``conftest.py``::

    @pytest.fixture(scope='session')
    def event_loop(request):
        loop = asyncio.get_event_loop_policy().get_event_loop()
        yield loop
        loop.close()

``conftest.py``::

    @pytest.fixture
    def wse(event_loop):
        # The app icon is cached; purge the app icon cache if it exists
        try:
            del toga.Icon.__APP_ICON
        except AttributeError:
            pass

        return WSE(formal_name='Test App', app_id='org.beeware.toga.test-app')


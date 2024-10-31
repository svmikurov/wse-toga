import asyncio

import pytest

import toga

from wse.app import WSE


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def wse(event_loop):
    # The app icon is cached; purge the app icon cache if it exists
    try:
        del toga.Icon.__APP_ICON
    except AttributeError:
        pass

    return WSE(formal_name="Test App", app_id="org.beeware.toga.test-app")

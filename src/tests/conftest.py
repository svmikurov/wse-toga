import asyncio
from asyncio import AbstractEventLoop
from unittest.mock import patch, Mock, MagicMock

import pytest

import toga

from tests.utils import FixtureReader
from wse.app import WSE
from wse.page import MainBox

FIXTURE = 'params.json'
PARAMS = FixtureReader(FIXTURE).json()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
def wse(event_loop: AbstractEventLoop):
    """Return the application instance, fixture."""
    # The app icon is cached; purge the app icon cache if it exists
    try:
        del toga.Icon.__APP_ICON
    except AttributeError:
        pass

    return WSE(formal_name="Test App", app_id="org.beeware.toga.test-app")


@pytest.fixture(scope='function')
def selection_params(wse: WSE) -> None:
    """Populate exercise params selections form fixture."""
    wse.box_glossary_params.selection_start_period.set_items(
        PARAMS['exercise_choices']['edge_period_items'],
        PARAMS['lookup_conditions']['period_start_date'],
    )
    wse.box_glossary_params.selection_end_period.set_items(
        PARAMS['exercise_choices']['edge_period_items'],
        PARAMS['lookup_conditions']['period_end_date'],
    )
    wse.box_glossary_params.selection_category.set_items(
        PARAMS['exercise_choices']['categories'],
        PARAMS['lookup_conditions']['category'],
    )
    wse.box_glossary_params.selection_progress.set_items(
        PARAMS['exercise_choices']['progress'],
        PARAMS['lookup_conditions']['progress'],
    )
    wse.box_glossary_params.input_count_first.value = (
        PARAMS['lookup_conditions']['count_first']
    )
    wse.box_glossary_params.input_count_last.value = (
        PARAMS['lookup_conditions']['count_last']
    )

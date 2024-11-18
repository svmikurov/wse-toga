"""Test glossary exercise params handlers.

Testing:
 * Filling out ang reade the selections.
 * Count switching.
 * Request handler of save params.
"""

from unittest.mock import AsyncMock, patch
from urllib.parse import urljoin

from toga.sources import ListSource

from tests.utils import FixtureReader, run_until_complete
from wse.app import WSE
from wse.constants import HOST_API

REQEUST_PARAMS_URL = '/api/v1/glossary/params/'
REQEUST_EXERCISE_URL = '/api/v1/glossary/exercise/'
FIXTURE = 'params.json'
PARAMS = FixtureReader(FIXTURE).json()


def get_assertion(items: list, expected: ListSource) -> None:
    """Assert that selection item is equal."""
    for index, item in enumerate(items):
        assert item.alias == expected[index].alias
        assert item.humanly == expected[index].humanly


def test_selection_start_period_data(
    wse: WSE,
    selection_params: object,
) -> None:
    """Test filling the selection with start period."""
    selection = wse.box_glossary_params.selection_start_period
    # Choice by default.
    assert (
        selection.value.alias
        == PARAMS['lookup_conditions']['period_start_date']
    )
    # Choices.
    choices_start_date = ListSource(
        accessors=['alias', 'humanly'],
        data=PARAMS['exercise_choices']['edge_period_items'],
    )
    get_assertion(selection.items, choices_start_date)


def test_selection_end_period_data(wse: WSE, selection_params: object) -> None:
    """Test filling the selection with end period."""
    selection = wse.box_glossary_params.selection_end_period
    # Choice by default.
    assert (
        selection.value.alias == PARAMS['lookup_conditions']['period_end_date']
    )
    # Choices.
    choices_end_date = ListSource(
        accessors=['alias', 'humanly'],
        data=PARAMS['exercise_choices']['edge_period_items'],
    )
    get_assertion(selection.items, choices_end_date)


def test_selection_category_data(wse: WSE, selection_params: object) -> None:
    """Test filling the selection with category."""
    selection = wse.box_glossary_params.selection_category
    # Choice by default.
    assert selection.value.alias == PARAMS['lookup_conditions']['category']
    # Choices.
    choices_category = ListSource(
        accessors=['alias', 'humanly'],
        data=PARAMS['exercise_choices']['categories'],
    )
    get_assertion(selection.items, choices_category)


def test_selection_progress_data(wse: WSE, selection_params: object) -> None:
    """Test filling the selection with progress."""
    selection = wse.box_glossary_params.selection_progress
    # Choice by default.
    assert selection.value.alias == PARAMS['lookup_conditions']['progress']
    # Choices.
    choices_progress = ListSource(
        accessors=['alias', 'humanly'],
        data=PARAMS['exercise_choices']['progress'],
    )
    get_assertion(selection.items, choices_progress)


def test_input_count_first(wse: WSE, selection_params: object) -> None:
    """Test filling the input_count_first."""
    input_field = wse.box_glossary_params.input_count_first
    # Choice by default.
    assert input_field.value == PARAMS['lookup_conditions']['count_first']
    assert wse.box_glossary_params.count_first_switch.value is False


def test_input_count_last(wse: WSE, selection_params: object) -> None:
    """Test filling the input_count_last."""
    input_field = wse.box_glossary_params.input_count_last
    # Choice by default.
    assert input_field.value == PARAMS['lookup_conditions']['count_last']
    assert wse.box_glossary_params.count_first_switch.value is False


@patch('httpx.AsyncClient.put')
def test_save_params_handler(
    put: AsyncMock,
    selection_params: object,
    wse: WSE,
) -> None:
    """Test save exercise parameters handler."""
    # Click button.
    btn_save_params = wse.box_glossary_params.btn_save_params
    btn_save_params._impl.simulate_press()

    # Request to save params by url.
    expected_url = urljoin(HOST_API, REQEUST_PARAMS_URL)
    expected_json = {
        'period_start_date': 'NC',
        'period_end_date': 'DT',
        'category': None,
        'progress': 'S',
        'count_first': 0,
        'count_last': 0,
    }
    run_until_complete(wse)

    put.assert_awaited_with(expected_url, json=expected_json)

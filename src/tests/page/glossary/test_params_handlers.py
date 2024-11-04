"""Test glossary exercise params handlers."""

from unittest.mock import Mock, PropertyMock, call, patch
from urllib.parse import urljoin

from toga.sources import ListSource

from tests.utils import FixtureReader
from wse.app import WSE
from wse.constants import GLOSSARY_PARAMS_PATH, HOST_API

REQEUST_PARAMS_URL = '/api/v1/glossary/params/'
REQEUST_EXERCISE_URL = '/api/v1/glossary/exercise/'
FIXTURE = 'params_glossary.json'
PARAMS = FixtureReader(FIXTURE).json()


def get_assertion(items: list, expected: ListSource) -> None:
    """Assert that selection item is equal."""
    for index, item in enumerate(items):
        assert item.alias == expected[index].alias
        assert item.humanly == expected[index].humanly


@patch(
    target='wse.page.ParamGlossaryBox.lookup_conditions',
    new_callable=PropertyMock,
)
@patch(
    target='httpx.Client.get',
)
def test_on_open(get: Mock, lookup_conditions: Mock, wse: WSE) -> None:
    """Test the calls of on_open method glossary params box."""
    # Opening page requests the user exercise params from server.
    get.return_value = Mock(
        name='Response',
        status_code=200,
        json=Mock(return_value=PARAMS),
    )
    wse.box_glossary_params.on_open()

    # Exercise params request url.
    url = call(url=urljoin(HOST_API, GLOSSARY_PARAMS_PATH))
    assert get.call_args == url

    # Call lookup_condition property setter.
    mock_calls = [call(PARAMS)]
    assert lookup_conditions.mock_calls == mock_calls


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


@patch('httpx.Client.post')
def test_save_params_handler(
    post: Mock,
    selection_params: object,
    wse: WSE,
) -> None:
    """Test save exercise parameters handler."""
    # Click button.
    wse.box_glossary_params.btn_save_params._impl.simulate_press()

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
    post.assert_called_with(url=expected_url, json=expected_json)


def test_count_switch(wse: WSE) -> None:
    """Test the count switching."""
    box = wse.box_glossary_params
    # Switching by default.
    assert not box.count_first_switch.value
    assert not box.count_last_switch.value

    # Toggle the first switch to set True.
    box.count_first_switch.toggle()
    assert box.count_first_switch.value
    assert not box.count_last_switch.value

    # Toggle the last switch to True.
    box.count_last_switch.toggle()
    assert not box.count_first_switch.value
    assert box.count_last_switch.value

    # Toggle the last switch to set False.
    box.count_last_switch.toggle()
    assert not box.count_first_switch.value
    assert not box.count_last_switch.value

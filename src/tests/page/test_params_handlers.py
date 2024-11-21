"""Test glossary exercise params handlers.

Testing:
 * Filling out ang reade the selections.
 * Count switching.
 * Request handler of save params.

"""

from unittest.mock import MagicMock, Mock, PropertyMock, call, patch
from urllib.parse import urljoin

import pytest
from _pytest.fixtures import FixtureRequest
from toga.handlers import simple_handler
from toga.sources import ListSource

from tests.utils import FixtureReader
from wse.app import WSE
from wse.constants import HOST_API
from wse.pages import ParamForeignPage, ParamGlossaryPage

PARAMS = FixtureReader('params.json').json()


def get_assertion(items: list, expected: ListSource) -> None:
    """Assert that selection item is equal."""
    for index, item in enumerate(items):
        assert item.alias == expected[index].alias
        assert item.humanly == expected[index].humanly


@pytest.fixture
def box_foreign(wse: WSE) -> ParamForeignPage:
    """Return the instance of ParamForeignPage, fixture."""
    box = wse.box_foreign_params
    return box


@pytest.fixture
def box_glossary(wse: WSE) -> ParamGlossaryPage:
    """Return the instance of ParamGlossaryPage, fixture."""
    box = wse.box_glossary_params
    return box


@pytest.fixture(params=['box_foreign', 'box_glossary'])
def box(request: FixtureRequest) -> ParamForeignPage | ParamGlossaryPage:
    """Return the box fixtures one by one."""
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    'box_name, params_path, lookup_conditions',
    [
        (
            'box_foreign_params',
            '/api/v1/foreign/params/',
            'wse.page.ParamForeignPage.lookup_conditions',
        ),
        (
            'box_glossary_params',
            '/api/v1/glossary/params/',
            'wse.page.ParamGlossaryPage.lookup_conditions',
        ),
    ],
)
@patch('httpx.Client.get')
def test_on_open(
    get: MagicMock,
    box_name: str,
    lookup_conditions: str,
    params_path: str,
    wse: WSE,
) -> None:
    """Test the call of on_open method params box.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * that request specific url;
     * that that requested params has been set to
       lookup_condition property of class.

    """
    box: ParamForeignPage | ParamGlossaryPage = getattr(wse, box_name)
    url = urljoin(HOST_API, params_path)

    wrapped = simple_handler(box.on_open, box)

    # Opening page requests the source_user exercise params to server.
    get.return_value = Mock(
        name='Response',
        status_code=200,
        json=Mock(return_value=PARAMS),
    )

    # Mock the lookup_conditions.
    with patch(lookup_conditions, new_callable=PropertyMock) as mock:
        # Invoke on_open method.
        wse.loop.run_until_complete(wrapped(box))

        # Assert that request specific url.
        assert get.call_args == call(url=url)

        # Set requested params to lookup_condition property.
        assert mock.mock_calls == [call(PARAMS)]


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

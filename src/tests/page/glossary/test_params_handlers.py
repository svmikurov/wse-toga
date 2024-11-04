"""Test glossary exercise params handlers."""

from unittest.mock import Mock, PropertyMock, call, patch

from tests.utils import FixtureReader
from wse.app import WSE

FIXTURE = 'params_glossary.json'
PARAMS = FixtureReader(FIXTURE)


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
        json=Mock(return_value=PARAMS.json()),
    )
    wse.box_glossary_params.on_open()

    # Exercise params request url.
    url = call(url='http://127.0.0.1/api/v1/glossary/params/')
    assert get.call_args == url

    # Call lookup_condition property setter.
    mock_calls = [call(PARAMS.json())]
    assert lookup_conditions.mock_calls == mock_calls


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
    expected_url='http://127.0.0.1/api/v1/glossary/params/'
    expected_json={
            'period_start_date': 'NC',
            'period_end_date': 'DT',
            'category': 1,
            'progress': 'S',
            'count_first': 0,
            'count_last': 0,
        }
    post.assert_called_with(url=expected_url, json=expected_json)

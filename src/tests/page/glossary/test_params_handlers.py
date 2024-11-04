"""Test glossary exercise params handlers."""

from unittest.mock import Mock, call, patch

from tests.utils import FixtureReader
from wse.app import WSE

FIXTURE = 'params_glossary.json'
PARAMS = FixtureReader(FIXTURE).json()


@patch(target='httpx.Client.get')
def test_on_open(get: Mock, wse: WSE) -> None:
    """Test the calls of on_open method glossary params box."""
    get.return_value = Mock(
        name='Response',
        status_code=200,
        json=Mock(return_value=PARAMS),
    )
    wse.box_glossary_params.on_open()

    # Opening page requests the user exercise params from server.
    url = call(url='http://127.0.0.1/api/v1/glossary/params/')
    assert get.call_args == url

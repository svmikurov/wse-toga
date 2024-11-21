"""Unit tests of user source."""

from unittest.mock import patch

import pytest

from wse.app import WSE
from wse.source.user import UserSource


@pytest.fixture
def source() -> UserSource:
    """Return the user source instance, fixture."""
    return UserSource()


def test_create_instance(source: UserSource) -> None:
    """Test create the source instance."""
    assert source.username is None
    assert source.is_auth is False


def test_app_instance(wse: WSE) -> None:
    """Test of create user source instance at app."""
    assert hasattr(wse, 'user')
    assert wse.user.username is None
    assert wse.user.is_auth is False


def test_user_main_box(wse: WSE) -> None:
    """Test add user to main box."""
    assert hasattr(wse.box_main, 'user')


def test_calls_on_start_app() -> None:
    """Test the source calls on start app."""
    with patch('wse.source.user.UserSource.set_auth_data') as set_auth_data:
        WSE(formal_name='Test app', app_id='com.com')

        set_auth_data.assert_called_once()


def test_set_auth_data(source: UserSource) -> None:
    """Test set auth data method of source."""
    # Set for auth user.
    source._username = None
    source._is_auth = False

    source.set_auth_data('name')

    assert source.username == 'name'
    assert source.is_auth is True

    # Set for not auth user.
    source._username = 'name'
    source._is_auth = True

    source.set_auth_data()

    assert source.username is None
    assert source.is_auth is False

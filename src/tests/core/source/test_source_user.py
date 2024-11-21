"""Unit tests of user source."""

import pytest

from wse.app import WSE
from wse.source.user import UserSource


@pytest.fixture
def source() -> UserSource:
    """Return the source instance, fixture."""
    return UserSource()


def test_app_instance(wse: WSE) -> None:
    """Test create the source instance."""
    assert hasattr(wse, 'source_user')
    assert wse.source_user.username is None
    assert wse.source_user.is_auth is False


def test_source_main_box(wse: WSE) -> None:
    """Test add source to main box."""
    assert hasattr(wse.box_main, 'source_user')


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

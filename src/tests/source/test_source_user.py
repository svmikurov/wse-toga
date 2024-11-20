"""Unit tests of user source."""

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


def test_manage_attr(source: UserSource) -> None:
    """Test the manage of instance attrs."""
    source.username = 'Test name'
    source.is_auth = True
    assert source.username == 'Test name'
    assert source.is_auth is True


def test_app_instance(wse: WSE) -> None:
    """Test of create user source instance at app."""
    assert hasattr(wse, 'user')
    assert wse.user.username is None
    assert wse.user.is_auth is False


def test_user_main_box(wse: WSE) -> None:
    """Test add user to main box."""
    assert hasattr(wse.box_main, 'user')

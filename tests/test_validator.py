"""Test user credentials validator."""

import pytest

from wse.contrib.utils import validate_username, validate_password


@pytest.mark.parametrize(
    "test_input,expected",
    [('username', True), ('wrong!', False)]
)
def test_username_validator(test_input, expected):
    assert validate_username(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [('password', True), ('passwor', False), ('00000000', False)]
)
def test_password_validator(test_input, expected):
    assert validate_password(test_input) == expected

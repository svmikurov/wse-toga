"""Test user credentials validator."""

import pytest

from wse.contrib.validator import validate_username, validate_password


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('username', []),
        ('wrong!', ['Допустимы только буквы, цифры и символы @/./+/-/_.']),
        ('@.+-_1иG', []),
    ]
)
def test_username_validator(test_input, expected):
    assert validate_username(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('12345678', ['Пароль не может состоять только из цифр']),
        ('passwor', ['Пароль должен содержать как минимум 8 символов']),
        ('password', []),
    ]
)
def test_password_validator(test_input, expected):
    assert validate_password(test_input) == expected

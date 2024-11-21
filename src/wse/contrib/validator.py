"""Validators."""

CYRILLIC_LOWER = ''.join(chr(i) for i in range(1072, 1104))
CYRILLIC_UPPER = ''.join(chr(i) for i in range(1040, 1072))
LATIN_LOWER = ''.join(chr(i) for i in range(65, 90))
LATIN_UPPER = ''.join(chr(i) for i in range(97, 122))
NUMBERS = '0123456789'
SYMBOLS = '@.+-_'

MAX_USER_LENGTH = 150
MIN_PASSWORD_LENGTH = 8

SYMBOL_ERROR = 'Допустимы только буквы, цифры и символы @/./+/-/_.'
LENGTH_ERROR = 'Длина имени не должна превышать 150 символов.'
PASSWORD_LENGTH_ERROR = 'Пароль должен содержать как минимум 8 символов'


def validate_username(username: str) -> list:
    """Validate the username.

    >>> validate_username('username')
    []
    >>> validate_username('wrong!')
    ['Допустимы только буквы, цифры и символы @/./+/-/_.']
    >>> validate_username('@.+-_1иG')
    []
    """
    allowed = (
        CYRILLIC_LOWER
        + CYRILLIC_UPPER
        + LATIN_LOWER
        + LATIN_UPPER
        + NUMBERS
        + SYMBOLS
    )

    errors = []
    for liter in username:
        if liter not in allowed:
            errors.append(SYMBOL_ERROR)
            break

    if len(username) > MAX_USER_LENGTH:
        errors.append(LENGTH_ERROR)
    return errors


def validate_password(password: str) -> list:
    """Validate the source_user password.

    >>> validate_password('12345678')
    ['Пароль не может состоять только из цифр']
    >>> validate_password('xxx')
    ['Пароль должен содержать как минимум 8 символов']
    >>> validate_password('password')
    []
    """
    errors = ['Пароль не может состоять только из цифр']
    for item in password:
        if item not in NUMBERS:
            errors.pop()
            break

    if len(password) < MIN_PASSWORD_LENGTH:
        errors.append(PASSWORD_LENGTH_ERROR)

    return errors


def validate_credentials(credentials: dict) -> list:
    """Validate the source_user credentials."""
    errors = []
    errors.extend(validate_username(credentials['username']))
    errors.extend(validate_password(credentials['password']))
    return errors

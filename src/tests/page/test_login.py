"""Test Login widgets.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget count for test.

.. todo::

   * add test login - request to login.
"""

import pytest

from tests.utils import run_until_complete
from wse.app import WSE
from wse.general.goto_handler import goto_login_handler
from wse.page import LoginBox, MainBox

WIDGET_COUNT = 5
"""Widget count at testing box container (int).
"""


@pytest.fixture(autouse=True)
def move_login_page(wse: WSE) -> None:
    """Assign the login box to main window content, fixture."""
    wse.main_window.content = wse.box_login


@pytest.fixture
def box_login(wse: WSE) -> LoginBox:
    """Return log in box-container."""
    return wse.box_login


@pytest.fixture
def box_main(wse: WSE) -> MainBox:
    """Return main box-container."""
    return wse.box_main


def test_widget_count(box_login: LoginBox) -> None:
    """Test of widget count."""
    assert WIDGET_COUNT == len(box_login.children)


def test_title(box_login: LoginBox) -> None:
    """Test page box title."""
    assert box_login.label_title.text == 'Вход в учетную запись'


def test_username_input(box_login: LoginBox) -> None:
    """Test username input widget."""
    assert box_login.input_username.placeholder == 'Имя'


def test_password_input(box_login: LoginBox) -> None:
    """Test password input widget."""
    assert box_login.input_password.placeholder == 'Пароль'


def test_btn_goto_login(box_main: MainBox) -> None:
    """Test the button go to log in."""
    button = box_main.btn_goto_login
    assert button.text == 'Вход в учетную запись'
    assert button.on_press._raw == goto_login_handler


def test_btn_login(box_login: LoginBox) -> None:
    """Test the button to login."""
    button = box_login.btn_login
    assert button.text == 'Войти в учетную запись'
    assert button.on_press._raw == box_login.login_handler


def test_logout_btn(box_main: MainBox) -> None:
    """Test the button to logout."""
    button = box_main.btn_logout
    assert button.text == 'Выйти из учетной записи'
    assert button.on_press._raw == box_main.logout_handler


def test_goto_main_box_btn(wse: WSE) -> None:
    """Test the button to go to main page box."""
    button = wse.box_login.btn_goto_main
    button._impl.simulate_press()
    run_until_complete(wse)
    assert button.text == 'На главную'
    assert wse.main_window.content == wse.box_main

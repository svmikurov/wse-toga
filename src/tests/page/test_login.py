"""Test Login page box widgets.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget count for test.

.. todo::

   * add test login - request to login.
"""

import pytest

from wse.app import WSE

WIDGET_COUNT = 5
"""Widget count at testing box container (int).
"""


@pytest.fixture(autouse=True)
def goto_glossary_login_page(wse: WSE) -> None:
    """Assign the login box to main window content, fixture."""
    wse.main_window.content = wse.box_login


def test_widget_count(wse: WSE) -> None:
    """Test of widget count."""
    children = wse.box_login.children
    assert WIDGET_COUNT == len(children)


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.box_login.label_title
    assert title.text == 'Вход в учетную запись'


def test_username_input(wse: WSE) -> None:
    """Test username input widget."""
    input_username = wse.box_login.input_username
    assert input_username.placeholder == 'Имя'


def test_password_input(wse: WSE) -> None:
    """Test password input widget."""
    input_password = wse.box_login.input_password
    assert input_password.placeholder == 'Пароль'


def test_login_btn(wse: WSE) -> None:
    """Test the button to request login."""
    btn = wse.box_login.btn_submit
    assert btn.text == 'Войти'
    # btn._impl.simulate_press()
    # assert wse.main_window.content == wse.box_main


def test_goto_main_box_btn(wse: WSE) -> None:
    """Test the button to go to main page box."""
    btn = wse.box_login.btn_goto_main
    assert btn.text == 'На главную'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_main

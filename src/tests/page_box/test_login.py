"""Test Login page box widgets.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget count for test.

.. todo::

   * add test login - request to login.
"""

from wse.app import WSE

WIDGET_COUNT = 5
"""Widget count at testing box container (int).
"""


def test_widget_count(wse: WSE) -> None:
    """Test of widget count."""
    children = wse.login_box.children
    assert WIDGET_COUNT == len(children)


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.login_box.title_label
    assert title.text == 'Вход в учетную запись'


def test_username_input(wse: WSE) -> None:
    """Test username input widget."""
    username_input = wse.login_box.username_input
    assert username_input.placeholder == 'Имя'


def test_password_input(wse: WSE) -> None:
    """Test password input widget."""
    password_input = wse.login_box.password_input
    assert password_input.placeholder == 'Пароль'


def test_login_btn(wse: WSE) -> None:
    """Test the button to request login."""
    btn = wse.login_box.btn_submit
    assert btn.text == 'Войти'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.main_box


def test_goto_main_box_btn(wse: WSE) -> None:
    """Test the button to go to main page box."""
    btn = wse.login_box.btn_goto_main_box
    assert btn.text == 'На главную'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.main_box

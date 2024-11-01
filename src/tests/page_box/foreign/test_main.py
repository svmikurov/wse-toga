"""Test Foreign page box widgets.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget count for test.
"""

import pytest

from wse.app import WSE

WIDGET_COUNT = 5
"""Widget count at testing box container (int).
"""


@pytest.fixture(autouse=True)
def goto_foreign_page_box(wse: WSE) -> None:
    """Set foreign box to main window content."""
    wse.main_window.content = wse.foreign_box


def test_widget_count(wse: WSE) -> None:
    """Test of widget count."""
    children = wse.foreign_box.children
    assert WIDGET_COUNT == len(children)


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.foreign_box.title_label
    assert title.text == 'Иностранный словарь'


def test_goto_main_box_btn(wse: WSE) -> None:
    """Test button to go to main page box."""
    btn = wse.foreign_box.btn_goto_main
    assert btn.text == 'На главную'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.main_box


def test_goto_foreign_create_page_btn(wse: WSE) -> None:
    """Test button to go to foreign create page box."""
    btn = wse.foreign_box.btn_goto_create
    assert btn.text == 'Добавить слово'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_create_box


def test_goto_foreign_params_page_btn(wse: WSE) -> None:
    """Test button to go to foreign exercise params page box."""
    btn = wse.foreign_box.btn_goto_params
    assert btn.text == 'Упражнение'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_params_box


def test_goto_foreign_list_page_btn(wse: WSE) -> None:
    """Test button to go to term list page box."""
    btn = wse.foreign_box.btn_goto_list
    assert btn.text == 'Словарь'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_list_box

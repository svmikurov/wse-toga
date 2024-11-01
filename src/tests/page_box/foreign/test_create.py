"""Test widgets of create foreign word page box.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget order at page.
"""

import pytest

from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_foreign_create_page(wse: WSE) -> None:
    """Assign the foreign create box to main window content."""
    wse.main_window.content = wse.foreign_create_box


def test_widget_order(wse: WSE) -> None:
    """Test the widget orger at foreign create page box."""
    box = wse.foreign_create_box
    expected_widget_order = [
        box.title_label,
        box.russian_input,
        box.foreign_input,
        box.btn_submit,
        box.btn_goto_foreign_list_box,
        box.btn_goto_foreign_box,
    ]
    assert box.children == expected_widget_order


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.foreign_create_box.title_label
    assert title.text == 'Добавить слово'


def test_native_input(wse: WSE) -> None:
    """Test the native word input field."""
    russian_input = wse.foreign_create_box.russian_input
    assert russian_input.placeholder == 'Слово на русском'
    assert russian_input.enabled is True


def test_foreign_input(wse: WSE) -> None:
    """Test the foreign word input field."""
    foreign_input = wse.foreign_create_box.foreign_input
    assert foreign_input.placeholder == 'Слово на иностранном'
    assert foreign_input.enabled is True


def test_btn_submit(wse: WSE) -> None:
    """Test the submit button."""
    btn = wse.foreign_create_box.btn_submit
    assert btn.text == 'Добавить'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_create_box


def test_btn_goto_foreign_box(wse: WSE) -> None:
    """Test button to go to foreign page box."""
    btn = wse.foreign_create_box.btn_goto_foreign_box
    assert btn.text == 'Меню иностранные слова'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_box


def test_btn_goto_foreign_list_box(wse: WSE) -> None:
    """Test button to go to foreign list page box."""
    btn = wse.foreign_create_box.btn_goto_foreign_list_box
    assert btn.text == 'Словарь иностранных слов'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_list_box

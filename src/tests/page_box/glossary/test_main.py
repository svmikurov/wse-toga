"""Test the widgets of glossary main page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widgets at page.
"""

import pytest

from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_glossary_main_page(wse: WSE) -> None:
    """Assign the glossary main page box to main window content.

    The pytest fixture, ``autouse=True``.
    """
    wse.main_window.content = wse.glossary_box


def test_widget_order(wse: WSE) -> None:
    """Test the widget order at glossary main page box."""
    box = wse.glossary_box

    assert box.children == [
        box.title_label,
        box.btn_goto_main_box,
        box.btn_goto_create_box,
        box.btn_goto_params_box,
        box.btn_goto_list_box,
    ]


def test_label_title(wse: WSE) -> None:
    """Test the title of glossary term create page box."""
    title = wse.glossary_box.title_label
    assert title.text == 'Глоссарий'


def test_btn_goto_main_page(wse: WSE) -> None:
    """Test the button of go to main page box."""
    btn = wse.glossary_box.btn_goto_main_box
    assert btn.text == 'На главную'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.main_box


def test_btn_goto_glossary_create_page(wse: WSE) -> None:
    """Test the button of go to create glossary term page box."""
    btn = wse.glossary_box.btn_goto_create_box
    assert btn.text == 'Добавить термин'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_create_box


def test_btn_goto_glossary_params_page(wse: WSE) -> None:
    """Test the button of go to glossary exercise params page box."""
    btn = wse.glossary_box.btn_goto_params_box
    assert btn.text == 'Упражнение'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_params_box


def test_btn_goto_glossary_term_list_page(wse: WSE) -> None:
    """Test the button of go to glossary term list page box."""
    btn = wse.glossary_box.btn_goto_list_box
    assert btn.text == 'Глоссарий'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_list_box

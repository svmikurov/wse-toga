"""Tests of create word page box widgets.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

 .. todo::

   * add test glossary create - request create term.
   * add test glossary create - create term handler.
"""

import pytest

from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_glossary_term_create_page(wse: WSE) -> None:
    """Assign the glossary create page box to main windows content.

    The pytest fixture, ``autouse=True``.
    """
    wse.main_window.content = wse.glossary_create_box


def test_widget_order(wse: WSE) -> None:
    """Test the widget order at glossary term create page box."""
    box = wse.glossary_create_box

    assert box.children == [
        box.title_label,
        box.input_term,
        box.input_definition,
        box.btn_submit,
        box.btn_goto_glossary_list,
        box.btn_goto_glossary_main,
    ]


def test_label_title(wse: WSE) -> None:
    """Test the title of glossary term create page box."""
    title = wse.glossary_create_box.title_label
    assert title.text == 'Добавить термин'


def test_input_glossary_term(wse: WSE) -> None:
    """Test the term input field of glossary create page."""
    input_field = wse.glossary_create_box.input_term
    assert input_field.placeholder == 'Термин'
    assert input_field.readonly is False


def test_input_glossary_definition(wse: WSE) -> None:
    """Test the definition input field of glossary create page."""
    input_field = wse.glossary_create_box.input_definition
    assert input_field.placeholder == 'Определение'
    assert input_field.readonly is False


def test_btn_submit(wse: WSE) -> None:
    """Test the button of create glossary term create."""
    btn = wse.glossary_create_box.btn_submit
    assert btn.text == 'Добавить'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_create_box


def test_btn_goto_glossary_list_page(wse: WSE) -> None:
    """Test the button of go to glossary list page box."""
    btn = wse.glossary_create_box.btn_goto_glossary_list
    assert btn.text == 'Глоссарий'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_list_box


def test_btn_goto_glossary_main_page(wse: WSE) -> None:
    """Test the button of go to glossary main page."""
    btn = wse.glossary_create_box.btn_goto_glossary_main
    assert btn.text == 'Глоссарий меню'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_box

"""Tests of create word page box widgets.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.
"""

import asyncio

import pytest
from _pytest.monkeypatch import MonkeyPatch

from wse.app import WSE
from wse.general.table import TableApp


@pytest.fixture(autouse=True)
def goto_glossary_term_create_page(wse: WSE) -> None:
    """Assign the glossary create page box to main windows content.

    The pytest fixture, ``autouse=True``.
    """
    wse.main_window.content = wse.box_glossary_create


def test_widget_order(wse: WSE) -> None:
    """Test the widget order at glossary term create page box."""
    box = wse.box_glossary_create

    assert box.children == [
        box.label_title,
        box.input_term,
        box.input_definition,
        box.btn_submit,
        box.btn_goto_glossary_list,
        box.btn_goto_glossary_main,
    ]


def test_label_title(wse: WSE) -> None:
    """Test the title of glossary term create page box."""
    title = wse.box_glossary_create.label_title
    assert title.text == 'Добавить термин'


def test_input_term(wse: WSE) -> None:
    """Test the term input field of glossary create page."""
    input_field = wse.box_glossary_create.input_term
    assert input_field.placeholder == 'Термин'
    assert input_field.readonly is False


def test_input_definition(wse: WSE) -> None:
    """Test the definition input field of glossary create page."""
    input_field = wse.box_glossary_create.input_definition
    assert input_field.placeholder == 'Определение'
    assert input_field.readonly is False


def test_btn_submit(wse: WSE) -> None:
    """Test the button of create glossary term create."""
    btn = wse.box_glossary_create.btn_submit
    btn._impl.simulate_press()
    assert btn.text == 'Добавить'
    assert wse.main_window.content == wse.box_glossary_create


def request_entries(obj: object, url: str) -> list[tuple[str, str]]:
    """Return entries to insert at table."""
    return [
        ('term', 'definition'),
    ]


def test_btn_goto_glossary_list(
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the button of go to glossary list page box."""
    btn = wse.box_glossary_create.btn_goto_glossary_list

    monkeypatch.setattr(TableApp, 'request_entries', request_entries)

    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.2))

    assert btn.text == 'Словарь терминов'
    assert wse.main_window.content == wse.box_glossary_list


def test_btn_goto_glossary_main(wse: WSE) -> None:
    """Test the button of go to glossary main page."""
    btn = wse.box_glossary_create.btn_goto_glossary_main

    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.2))

    assert btn.text == 'Глоссарий'
    assert wse.main_window.content == wse.box_glossary_main

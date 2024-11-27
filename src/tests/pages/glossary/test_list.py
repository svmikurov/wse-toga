"""Test widgets of glossary term list page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.
"""

import pytest

from tests.utils import run_until_complete
from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_glossary_list_page(wse: WSE) -> None:
    """Assign the glossary list box to main window content, fixture."""
    wse.main_window.content = wse.box_glossary_list


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at glossary list page."""
    box = wse.box_glossary_list

    assert box.children == [
        box.label_title,
        box.btn_goto_glossary_main,
        box.btns_manage,
        box.table,
        box.btns_paginate,
    ]

    assert box.btns_manage.children == [
        box._btn_create,
        box._btn_update,
        box._btn_delete,
    ]

    assert box.btns_paginate.children == [
        box._btn_previous,
        box._btn_table_reload,
        box._btn_next,
    ]


def test_label_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.box_glossary_list.label_title
    assert title.text == 'Список терминов'


def test_table(wse: WSE) -> None:
    """Test table of glossary term list."""
    table = wse.box_glossary_list.table
    assert table.headings == ['ID', 'Термин', 'Толкование']
    assert table.accessors == ['id', 'term', 'definition']


def test_btn_goto_glossary_main(wse: WSE) -> None:
    """Test button to go to glossary main page box."""
    btn = wse.box_glossary_list.btn_goto_glossary_main

    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Глоссарий'
    assert wse.main_window.content == wse.box_glossary_main

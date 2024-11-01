"""Test widgets of glossary term list page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

.. todo::

   * add test glossary term list - request term list;
   * add test glossary term list - update and delete term buttons;
   * add test glossary term list - update and delete term handlers;
   * add test glossary term list - pagination buttons, handlers.
"""

import pytest

from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_glossary_list_page(wse: WSE) -> None:
    """Assign the glossary list box to main window content, fixture."""
    wse.main_window.content = wse.glossary_list_box


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at glossary list page."""
    box = wse.glossary_list_box

    assert box.children == [
        box.title_label,
        box.btn_goto_glossary_box,
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


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.glossary_list_box.title_label
    assert title.text == 'Список терминов'


def test_table(wse: WSE) -> None:
    """Test table of glossary term list."""
    table = wse.glossary_list_box.table
    assert table.headings == ['Термин', 'Толкование']
    assert table.accessors == ['term', 'definition']


def test_btn_goto_glossary_box(wse: WSE) -> None:
    """Test button to go to glossary main page box."""
    btn = wse.glossary_list_box.btn_goto_glossary_box
    assert btn.text == 'Оглавление глоссария'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_box

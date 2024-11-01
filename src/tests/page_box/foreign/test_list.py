"""Test widgets of foreign word list page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

.. todo::

   * add test foreign word list - request word list;
   * add test foreign word list - update and delete word buttons;
   * add test foreign word list - update and delete word handlers;
   * add test foreign word list - pagination buttons, handlers.
"""

import pytest

from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_foreign_list_page(wse: WSE) -> None:
    """Assign the foreign list box to main window content, fixture."""
    wse.main_window.content = wse.foreign_list_box


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at foreign list page."""
    box = wse.foreign_list_box

    assert box.children == [
        box.label_title,
        box.btn_goto_foreign_box,
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
    title = wse.foreign_list_box.label_title
    assert title.text == 'Список иностранных слов'


def test_table(wse: WSE) -> None:
    """Test table of foreign word list."""
    table = wse.foreign_list_box.table
    assert table.headings == ['Иностранный', 'Русский']
    assert table.accessors == ['foreign_word', 'russian_word']


def test_btn_goto_foreign_box(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.foreign_list_box.btn_goto_foreign_box
    assert btn.text == 'Оглавление словаря'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_box

"""Test widgets of foreign word list page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget).
 * Changing window contents when pressing move buttons.
 * The order of widget and widget containers at page.
"""

import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import Client

from tests.utils import FixtureReader
from wse.app import WSE

FIXTURE_FOREIGN_LIST = 'response_foreign_list.json'
"""The fixture file name of json http response with a list of word
(`str`).
"""
FIXTURE_PAGINATION_FIRST = 'pagination_foreign_first.json'
"""The fixture file name to test the first pagination page (`str`)."""
FIXTURE_PAGINATION_LAST = 'pagination_foreign_last.json'
"""The fixture file name to test the last pagination page (`str`)."""


@pytest.fixture(autouse=True)
def goto_foreign_list_page(wse: WSE) -> None:
    """Assign the foreign list box to main window content, fixture."""
    wse.main_window.content = wse.box_foreign_list


def mock_list_json(*args: object, **kwargs: object) -> FixtureReader:
    """Mock a json http response with a list of terms."""
    return FixtureReader(FIXTURE_FOREIGN_LIST)


@pytest.fixture(autouse=True)
def populate_table(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Populate foreign word list table."""
    # Mock http request word list, populate table.
    monkeypatch.setattr(Client, 'get', mock_list_json)
    wse.box_foreign_list.populate_table()


def mock_pagination_first(*args: object, **kwargs: object) -> FixtureReader:
    """Mock a json http response to test the first pagination page."""
    return FixtureReader(FIXTURE_PAGINATION_FIRST)


def mock_pagination_last(*args: object, **kwargs: object) -> FixtureReader:
    """Mock a json http response to test the last pagination page."""
    return FixtureReader(FIXTURE_PAGINATION_LAST)


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at foreign list page."""
    box = wse.box_foreign_list

    assert box.children == [
        box.label_title,
        box.btn_goto_foreign_main,
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


def test_table(wse: WSE) -> None:
    """Test table of foreign word list."""
    table = wse.box_foreign_list.table
    assert table.headings == ['Иностранный', 'Русский']
    assert table.accessors == ['foreign_word', 'native_word']


def test_populate_table(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the populate foreign word list table."""
    entry_index = 0
    entry = wse.box_foreign_list.table.data._words[entry_index]
    assert entry.foreign_word == 'hello'
    assert entry.native_word == 'привет'


def test_label_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.box_foreign_list.label_title
    assert title.text == 'Словарь иностранных слов'


def test_btn_goto_foreign(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.box_foreign_list.btn_goto_foreign_main
    assert btn.text == 'Иностранный'

    # Window switching.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_main


def test_btn_goto_foreign_create(wse: WSE) -> None:
    """Test the button go to create foreign word."""
    btn = wse.box_foreign_list._btn_create
    assert btn.text == 'Добавить'

    # Window switching.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_create


def test_btn_goto_foreign_update(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the button go to update foreign word page box."""
    btn = wse.box_foreign_list._btn_update
    assert btn.text == 'Изменить'

    # Window switching.
    # Select table entry to update.
    entry_index = 1
    table = wse.box_foreign_list.table
    table._impl.simulate_selection(entry_index)
    # Press button.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_update


def test_btn_foreign_delete(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the button of delete foreign word."""
    btn = wse.box_foreign_list._btn_delete
    assert btn.text == 'Удалить'

    # No window switching.
    # Select table entry to delete.
    entry_index = 1
    table = wse.box_foreign_list.table
    table._impl.simulate_selection(entry_index)
    # Press button.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_list

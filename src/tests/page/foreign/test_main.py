"""Test foreign main page box widgets.

Testing:
 * Text representation of widgets in the window content
   (text on widget).
 * Changing window contents when pressing move buttons.
 * The order of widget at page.
"""

import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import Client

from tests.mocking import MockClient
from wse.app import WSE

FIXTURE = 'response_foreign_list.json'
"""The fixture file name of json http response with a list of word
(`str`).
"""


@pytest.fixture(autouse=True)
def goto_foreign_page_box(wse: WSE) -> None:
    """Assign the foreign main box to main window content, fixture."""
    wse.main_window.content = wse.box_foreign_main


def mock_list_json(*args: object, **kwargs: object) -> MockClient:
    """Mock a json http response with a list of terms."""
    return MockClient(FIXTURE)


def test_widget_order(wse: WSE) -> None:
    """Test the widget orger at foreign main page."""
    box = wse.box_foreign_main

    assert box.children == [
        box.label_title,
        box.btn_goto_main,
        box.btn_goto_create,
        box.btn_goto_params,
        box.btn_goto_list,
    ]


def test_label_title(wse: WSE) -> None:
    """Test label of page box title."""
    # Label text.
    title = wse.box_foreign_main.label_title
    assert title.text == 'Иностранный словарь'


def test_btn_goto_main(wse: WSE) -> None:
    """Test the button go to main page box."""
    btn = wse.box_foreign_main.btn_goto_main
    assert btn.text == 'На главную'

    # Window switching.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_main


def test_btn_goto_create(wse: WSE) -> None:
    """Test the button go to foreign create page box."""
    btn = wse.box_foreign_main.btn_goto_create
    assert btn.text == 'Добавить слово'

    # Window switching.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_create


def test_btn_goto_params(wse: WSE) -> None:
    """Test the button go to foreign exercise params page box."""
    btn = wse.box_foreign_main.btn_goto_params
    assert btn.text == 'Упражнение'

    # Window switching.
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_params


def test_btn_goto_list(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the button go to foreign word list page box."""
    btn = wse.box_foreign_main.btn_goto_list
    assert btn.text == 'Словарь'

    # Window switching.
    # Switching to the list page calls the http request of word list to
    # populate the table.
    # If mapping of word list have not required fields will be raising
    # the KeyError.
    monkeypatch.setattr(Client, 'get', mock_list_json)
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_list

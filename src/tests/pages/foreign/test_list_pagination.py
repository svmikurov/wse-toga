"""Test pagination buttons of foreign word list page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Button handlers.
"""

from unittest.mock import MagicMock, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch
from httpx import Client

from tests.utils import FixtureReader
from wse.app import WSE

FIXTURE_PAGINATION_FIRST = 'pagination_foreign_first.json'
"""The fixture file name to test the first pagination page (`str`)."""
FIXTURE_PAGINATION_LAST = 'pagination_foreign_last.json'
"""The fixture file name to test the last pagination page (`str`)."""


@pytest.fixture(autouse=True)
def goto_foreign_list_page(wse: WSE) -> None:
    """Assign the foreign list box to main window content, fixture."""
    wse.main_window.content = wse.box_foreign_list


def mock_pagination_first(*args: object, **kwargs: object) -> FixtureReader:
    """Mock a json http response to test the first pagination page."""
    return FixtureReader(FIXTURE_PAGINATION_FIRST)


def mock_pagination_last(*args: object, **kwargs: object) -> FixtureReader:
    """Mock a json http response to test the last pagination page."""
    return FixtureReader(FIXTURE_PAGINATION_LAST)


def test_pagination_first_page(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test pagination buttons at first page."""
    # Mock http request word list, populate table.
    monkeypatch.setattr(Client, 'get', mock_pagination_first)
    wse.box_foreign_list.populate_table()

    # Previous button.
    btn_previous = wse.box_foreign_list._btn_previous
    assert btn_previous.enabled is False

    # Next button.
    btn_next = wse.box_foreign_list._btn_next
    assert btn_next.enabled is True


def test_pagination_last_page(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test pagination buttons at last page."""
    # Mock http request word list, populate table.
    monkeypatch.setattr(Client, 'get', mock_pagination_last)
    wse.box_foreign_list.populate_table()

    # Previous button.
    btn_previous = wse.box_foreign_list._btn_previous
    assert btn_previous.enabled is True

    # Next button.
    btn_next = wse.box_foreign_list._btn_next
    assert btn_next.enabled is False


@patch('httpx.Client')
def test_btn_next_handler(client: MagicMock, wse: WSE) -> None:
    """Test the handler of button pagination next."""
    btn = wse.box_foreign_list._btn_next
    assert btn.text == '>'

    btn.enabled = True
    btn._impl.simulate_press()
    assert client.called


@patch('httpx.Client')
def test_btn_previous_handler(client: MagicMock, wse: WSE) -> None:
    """Test the handler of button pagination previous."""
    btn = wse.box_foreign_list._btn_previous
    assert btn.text == '<'

    btn.enabled = True
    btn._impl.simulate_press()
    assert client.called


@patch('httpx.Client')
def test_btn_table_reload_handler(client: MagicMock, wse: WSE) -> None:
    """Test the handler of button pagination previous."""
    btn = wse.box_foreign_list._btn_table_reload
    assert btn.text == 'Обновить'

    btn.enabled = True
    btn._impl.simulate_press()
    assert client.called

"""Test Main page box widgets.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget count for test.
"""
from unittest.mock import patch, MagicMock, AsyncMock

from toga.handlers import simple_handler

from tests.utils import run_until_complete
from wse.app import WSE
from wse.constants import HOST_API
from wse.general.goto_handler import goto_foreign_exercise

WIDGET_COUNT = 8
"""Widget count at testing box container (int).
"""


def test_widget_count(wse: WSE) -> None:
    """Test of widget count."""
    children = wse.box_main.children
    assert WIDGET_COUNT == len(children)


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.box_main.label_title
    assert title.text == 'WSELFEDU'


def test_btn_login(wse: WSE) -> None:
    """Test click on button to go to login page box."""
    btn = wse.box_main.btn_change_auth

    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Вход в учетную запись'
    assert wse.main_window.content == wse.box_login


def test_btn_goto_foreign_main(wse: WSE) -> None:
    """Test click on button to go to foreign page box."""
    btn = wse.box_main.btn_goto_foreign_main

    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Иностранный'
    assert wse.main_window.content == wse.box_foreign_main


def test_btn_goto_glossary_main(wse: WSE) -> None:
    """Test click on button to go to glossary page box."""
    btn = wse.box_main.btn_goto_glossary_main

    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Глоссарий'
    assert wse.main_window.content == wse.box_glossary_main


def test_info_panel(wse: WSE) -> None:
    """Test info panel placeholder."""
    info_panel = wse.box_main.info_panel
    assert info_panel.placeholder == f'Ready for connect to {HOST_API}'


def test_btn_goto_foreign_exercise(wse: WSE) -> None:
    """Test quik start button of foreign exercise."""
    btn = wse.box_main.btn_goto_foreign_exercise

    # Button has specific text.
    assert btn.text == 'Изучение слов'

    # Invoke the callback.
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    # Window switch.
    assert wse.main_window.content == wse.box_foreign_exercise


def test_btn_goto_glossary_exercise(wse: WSE) -> None:
    """Test quik start button of glossary exercise."""
    btn = wse.box_main.btn_goto_glossary_exercise

    # Button has specific text.
    assert btn.text == 'Изучение терминов'

    # Invoke the callback.
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    # Window switch.
    assert wse.main_window.content == wse.box_glossary_exercise

"""Test Main page box widgets.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget count for test.
"""

import asyncio

from wse.app import WSE
from wse.constants import HOST_API

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
    btn = wse.box_main.btn_goto_auth

    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.2))

    assert btn.text == 'Вход в учетную запись'
    assert wse.main_window.content == wse.box_login


def test_click_goto_foreign_btn(wse: WSE) -> None:
    """Test click on button to go to foreign page box."""
    btn = wse.box_main.btn_goto_foreign_main

    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.2))

    assert btn.text == 'Иностранный'
    assert wse.main_window.content == wse.box_foreign_main


def test_click_goto_glossary_btn(wse: WSE) -> None:
    """Test click on button to go to glossary page box."""
    btn = wse.box_main.btn_goto_glossary_main

    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.2))

    assert btn.text == 'Глоссарий'
    assert wse.main_window.content == wse.box_glossary_main


def test_info_panel(wse: WSE) -> None:
    """Test info panel placeholder."""
    info_panel = wse.box_main.info_panel
    assert info_panel.placeholder == f'Ready for connect to {HOST_API}'

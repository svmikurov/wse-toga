"""Test Main page box widgets."""

from wse.app import WSE
from wse.constants import HOST_API


def test_widget_count(wse: WSE) -> None:
    """Test of widget count."""
    widget_count = 5
    children = wse.main_box.children
    assert widget_count == len(children)


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.main_box.title_label
    assert title.text == 'WSELFEDU'


def test_click_goto_login_btn(wse: WSE) -> None:
    """Test click on button to go to login page box."""
    btn = wse.main_box.btn_goto_auth
    assert btn.text == 'Вход в учетную запись'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.login_box


def test_click_goto_foreign_btn(wse: WSE) -> None:
    """Test click on button to go to foreign page box."""
    btn = wse.main_box.btn_goto_foreign_box
    assert btn.text == 'Словарь иностранных слов'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_box


def test_click_goto_glossary_btn(wse: WSE) -> None:
    """Test click on button to go to glossary page box."""
    btn = wse.main_box.btn_goto_glossary_box
    assert btn.text == 'Глоссарий терминов'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_box


def test_info_panel(wse: WSE) -> None:
    """Test info panel placeholder."""
    info_panel = wse.main_box.info_panel
    assert info_panel.placeholder == f'Ready for connect to {HOST_API}'

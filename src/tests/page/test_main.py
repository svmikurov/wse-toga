"""Test Main page box widgets.

Test:
 * the representation of widgets in the window content;
 * the widget count at main page;
 * that button has specific content.
"""

from typing import Callable

import pytest

from wse.app import WSE
from wse.constants import HOST_API
from wse.general import goto_handler as hl

WIDGET_COUNT = 8
"""Widget count at testing box container (int).
"""


def test_widget_count(wse: WSE) -> None:
    """Test of widget count."""
    children = wse.box_main.children
    assert WIDGET_COUNT == len(children)


def test_label_title(wse: WSE) -> None:
    """Test page box title."""
    label_title = wse.box_main.label_title
    assert label_title.text == 'WSELFEDU'


def test_info_panel(wse: WSE) -> None:
    """Test info panel placeholder."""
    info_panel = wse.box_main.info_panel
    assert info_panel.placeholder == f'Ready for connect to {HOST_API}'


def test_label_chapter_exercises(wse: WSE) -> None:
    """Test the label of exercise buttons."""
    label_chapter_exercises = wse.box_main.label_chapter_exercises
    assert label_chapter_exercises.text == 'Упражнения:'


@pytest.mark.parametrize(
    'button_name, button_text, button_handler',
    [
        ('btn_goto_foreign_main', 'Иностранный', hl.goto_foreign_main_handler),
        (
            'btn_goto_glossary_main',
            'Глоссарий',
            hl.goto_glossary_main_handler,
        ),
        (
            'btn_goto_foreign_exercise',
            'Изучение слов',
            hl.goto_foreign_exercise_handler,
        ),
        (
            'btn_goto_glossary_exercise',
            'Изучение терминов',
            hl.goto_glossary_exercise_handler,
        ),
    ],
)
def test_btn_goto_foreign_main(
    button_name: str, button_text: str, button_handler: Callable, wse: WSE
) -> None:
    """Test quik start button of glossary exercise."""
    btn = getattr(wse.box_main, button_name)

    # Button has specific text.
    assert btn.text == button_text

    # Button has callback.
    assert btn.on_press._raw is button_handler

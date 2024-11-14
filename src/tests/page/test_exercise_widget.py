"""Test widgets of foreign exercise page box.

.. todo::

   * add test the display a task question and answer;
   * add test the title label.

"""

from unittest.mock import AsyncMock, Mock, call, patch
from urllib.parse import urljoin

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch

from tests.utils import run_until_complete
from wse.app import WSE
from wse.constants import HOST_API
from wse.container.exercise import (
    AnswerBtn,
    ExerciseBox,
)
from wse.contrib.task import Task
from wse.contrib.timer import Timer
from wse.page import (
    ExerciseForeignPage,
    ExerciseGlossaryPage,
)


def set_window_content(
    wse: WSE,
    box: ExerciseForeignPage | ExerciseGlossaryPage,
) -> None:
    """Assign the box with widgets to window content."""
    wse.main_window.content = box


@pytest.fixture(autouse=True)
def box_foreign(wse: WSE) -> ExerciseForeignPage:
    """Return the instance of ExerciseForeignPage, fixture."""
    box = wse.box_foreign_exercise
    return box


@pytest.fixture
def box_glossary(wse: WSE) -> ExerciseGlossaryPage:
    """Return the instance of ExerciseForeignPage, fixture."""
    box = wse.box_glossary_exercise
    return box


@pytest.fixture(params=['box_foreign', 'box_glossary'])
def box(request: FixtureRequest) -> ExerciseForeignPage | ExerciseGlossaryPage:
    """Return the box fixtures one by one."""
    return request.getfixturevalue(request.param)


def test_foreign_widget_order(box_foreign: ExerciseForeignPage) -> None:
    """Test the widget and containers orger at foreign exercise page."""
    # Probably will use ``box`` fixture.
    box = box_foreign
    assert box.children == [
        box.label_title,
        box.box_exercise,
        box.btn_goto_params,
    ]
    assert box.box_exercise.children == [
        box.label_question,
        box.display_question,
        box.label_answer,
        box.display_answer,
        box.label_textpanel,
        box.display_exercise_info,
        box.box_btn_group,
    ]
    assert box.box_btn_group.children == [
        box.btn_pause,
        box.btn_not_know,
        box.btn_know,
        box.btn_next,
    ]


def test_glossary_widget_order(box_glossary: ExerciseGlossaryPage) -> None:
    """Test the widget and container orger at glossary exercise page."""
    # Probably will use ``box`` fixture.
    box = box_glossary

    assert box.children == [
        box.label_title,
        box.box_exercise,
        box.btn_goto_params,
    ]
    assert box.box_exercise.children == [
        box.label_question,
        box.display_question,
        box.label_answer,
        box.display_answer,
        box.box_btn_group,
    ]
    assert box.box_btn_group.children == [
        box.btn_pause,
        box.btn_not_know,
        box.btn_know,
        box.btn_next,
    ]


def test_display_question(
    box: ExerciseForeignPage | ExerciseGlossaryPage,
) -> None:
    """Test the question display.

    Testing:
     * ExerciseForeignPage and ExerciseGlossaryPage classes;
     * that the widget is read only.

    """
    # The display widget is read-only.
    assert box.display_question.readonly is True


def test_display_answer(
    box: ExerciseForeignPage | ExerciseGlossaryPage,
) -> None:
    """Test the question answer.

    Testing:
     * ExerciseForeignPage and ExerciseGlossaryPage classes;
     * that the widget is read only.

    """
    # The display widget is read-only.
    assert box.display_answer.readonly is True


def test_display_exercise_info(box_foreign: ExerciseForeignPage) -> None:
    """Test the exercise info display.

    Testing:
     * ExerciseForeignPage class;
     * that the widget is read only.

    """
    # The display widget is read-only.
    assert box_foreign.display_exercise_info.readonly is True


@patch.object(Timer, 'on_pause')
def test_btn_pause(on_pause: Mock, box: ExerciseBox) -> None:
    """Test the button of pause.

    Testing:
     * ExerciseForeignPage and ExerciseGlossaryPage classes;
     * call the ``on_pause`` method of the ``Timer`` class
       with the button handler when the button is pressed.

    """
    btn = box.btn_pause
    assert btn.text == 'Пауза'

    # Simulate a button press.
    btn._impl.simulate_press()

    # Assertion that the pause method of the Timer class was called.
    on_pause.assert_called()


@pytest.mark.parametrize(
    'box_name, btn_name, btn_text, action, request_path',
    [
        (
            'box_foreign_exercise',
            'btn_not_know',
            'Не знаю',
            'not_know',
            'api/v1/foreign/assessment/',
        ),
        (
            'box_foreign_exercise',
            'btn_know',
            'Знаю',
            'know',
            'api/v1/foreign/assessment/',
        ),
        (
            'box_glossary_exercise',
            'btn_not_know',
            'Не знаю',
            'not_know',
            'api/v1/glossary/progress/',
        ),
        (
            'box_glossary_exercise',
            'btn_know',
            'Знаю',
            'know',
            'api/v1/glossary/progress/',
        ),
    ],
)
@patch('httpx.AsyncClient.post', new_callable=AsyncMock)
@patch.object(ExerciseBox, 'move_to_next_task', new_callable=AsyncMock)
def test_answer_btns(
    move_to_next_task: AsyncMock,
    post: AsyncMock,
    box_name: str,
    btn_name: str,
    btn_text: str,
    action: str,
    request_path: str,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the buttons of answer.

    Testing:
     * ExerciseForeignPage and ExerciseGlossaryPage classes;
     * press ``know`` and `not_know`` buttons;
     * http request to answer.

     .. todo:

        * add test the change of task.status to 'question'.

    """
    box: ExerciseForeignPage | ExerciseGlossaryPage = getattr(wse, box_name)
    btn: AnswerBtn = getattr(box, btn_name)
    set_window_content(wse, box)

    # Mock the item ID to answer.
    monkeypatch.setattr(Task, 'item_id', 1)

    # Simulate a button press.
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    # Button has specific text.
    assert btn.text == btn_text

    # The button handler coroutine invoke http post request.
    assert post.call_args == call(
        urljoin(HOST_API, request_path),
        json={'action': action, 'item_id': 1},
    )
    # The button handler coroutine invoke the next task.
    move_to_next_task.assert_awaited()


@patch.object(ExerciseBox, 'loop_task', new_callable=AsyncMock)
def test_btn_next(
    loop_task: AsyncMock,
    box: ExerciseForeignPage | ExerciseGlossaryPage,
    wse: WSE,
) -> None:
    """Test the button of next task.

    :param AsyncMock loop_task: Mock a task loop method on button click.
    :param box: The box-container of tested widget, fixture.
    :type box: ExerciseForeignPage | ExerciseGlossaryPage

    Testing:
     * ExerciseForeignPage and ExerciseGlossaryPage classes;
     * button text;
     * that button handler invoke the coroutine of task loop.

    .. todo::

       * add test the unpause of task.

    """
    btn = box.btn_next
    set_window_content(wse, box)

    # Simulate a button press.
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    # Button text.
    assert box.btn_next.text == 'Далее'

    # The button handler coroutine invoke the next task.
    loop_task.assert_awaited()


@pytest.mark.parametrize(
    'box_name, box_togo',
    [
        ('box_glossary_exercise', 'box_glossary_params'),
        ('box_foreign_exercise', 'box_foreign_params'),
    ],
)
def test_btn_goto_params(
    box_name: str,
    box_togo: str,
    wse: WSE,
) -> None:
    """Test the button go to exercise params page.

    Testing:
     * ExerciseForeignPage and ExerciseGlossaryPage classes;
     * window switching.

    """
    box: ExerciseForeignPage | ExerciseGlossaryPage = getattr(wse, box_name)
    btn = box.btn_goto_params
    set_window_content(wse, box)

    # Simulate the press button.
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    # Button text.
    assert btn.text == 'Параметры упражнения'

    # Window switching.
    assert wse.main_window.content == getattr(wse, box_togo)

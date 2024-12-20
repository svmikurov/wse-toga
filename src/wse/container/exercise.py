"""Container for choice exercise progress parameter.

For exercises:
    * Glossary term study exercise
    * Foreign word study exercise
"""

from http import HTTPStatus

import toga
from toga.style.pack import COLUMN, ROW, Pack

from wse.constants import (
    ACTION,
    ANSWER,
    CATEGORIES,
    CATEGORY,
    EDGE_PERIODS,
    EXERCISE_CHOICES,
    KNOW,
    LOOKUP_CONDITIONS,
    NO_TASK_MSG,
    NOT_KNOW,
    PERIOD_END,
    PERIOD_START,
    PROGRESS,
    QUESTION,
    TASK_ERROR_MSG,
)
from wse.constants.literal import ITEM_ID
from wse.contrib.http_requests import request_post, request_post_async
from wse.contrib.task import Task
from wse.contrib.timer import Timer
from wse.general.box import FlexBox
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.label import TitleLabel
from wse.general.selection import BaseSelection
from wse.general.text_input import TextPanel


class AnswerBtn(toga.Button):
    """User answer button."""

    def __init__(
        self,
        text: str | None = None,
        on_press: toga.widgets.button.OnPressHandler | None = None,
    ) -> None:
        """Construct the button."""
        style = Pack(
            flex=1,
            height=100,
            font_size=9,
        )
        super().__init__(text=text, style=style, on_press=on_press)


class ExerciseParamSelectionsBox(BoxApp):
    """Exercise param box of selection widgets."""

    title = ''
    """Page box title (`str`).
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.style.update(direction=COLUMN)

        # Styles.
        style_label = Pack(padding=(7, 0, 7, 20))
        style_box_selection = Pack(padding=(2, 0, 2, 0))

        self.label_title = TitleLabel(text=self.title)

        # General buttons.
        self.btn_save_params = BtnApp(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )
        self.btn_goto_exercise = BtnApp(
            'Начать упражнение',
            on_press=self.goto_box_exercise_handler,
        )

        # Selection labels.
        self.label_start = toga.Label('Начало периода:', style=style_label)
        self.label_end = toga.Label('Конец периода:', style=style_label)
        self.label_category = toga.Label('Категория:', style=style_label)
        self.label_progres = toga.Label('Стадия изучения:', style=style_label)
        # Switch
        self.count_first_switch = toga.Switch(
            'Первые', style=style_label, on_change=self.first_switch_handler
        )
        self.count_last_switch = toga.Switch(
            'Последние', style=style_label, on_change=self.last_switch_handler
        )
        # Selections.
        self.selection_start_period = BaseSelection()
        self.selection_end_period = BaseSelection()
        self.selection_category = BaseSelection()
        self.selection_progress = BaseSelection()
        self.input_count_first = toga.NumberInput(step=10, min=0)
        self.input_count_last = toga.NumberInput(step=10, min=0)
        # Selection boxes.
        self.box_selection_start = toga.Box(
            style=style_box_selection,
            children=[
                FlexBox(children=[self.label_start]),
                FlexBox(children=[self.selection_start_period]),
            ],
        )
        self.box_selection_start.style.padding_top = 4
        self.box_selection_end = toga.Box(
            style=style_box_selection,
            children=[
                FlexBox(children=[self.label_end]),
                FlexBox(children=[self.selection_end_period]),
            ],
        )
        self.box_selection_category = toga.Box(
            style=style_box_selection,
            children=[
                FlexBox(children=[self.label_category]),
                FlexBox(children=[self.selection_category]),
            ],
        )
        self.box_selection_progress = toga.Box(
            style=style_box_selection,
            children=[
                FlexBox(children=[self.label_progres]),
                FlexBox(children=[self.selection_progress]),
            ],
        )
        self.box_input_first = toga.Box(
            style=style_box_selection,
            children=[
                FlexBox(
                    children=[self.count_first_switch],
                    style=Pack(direction=COLUMN, padding_right=20),
                ),
                FlexBox(
                    children=[self.input_count_first],
                    style=Pack(direction=COLUMN),
                ),
            ],
        )
        self.box_input_last = toga.Box(
            style=style_box_selection,
            children=[
                FlexBox(
                    children=[self.count_last_switch],
                    style=Pack(direction=COLUMN, padding_right=20),
                ),
                FlexBox(
                    children=[self.input_count_last],
                    style=Pack(direction=COLUMN),
                ),
            ],
        )

        # Widgets DOM.
        # Add ``params_box`` attr.
        self.box_params = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.add(
            self.label_title,
            self.box_params,
            self.btn_goto_exercise,
            self.btn_save_params,
        )
        self.box_params.add(
            self.box_selection_start,
            self.box_selection_end,
            self.box_selection_category,
            self.box_selection_progress,
            self.box_input_first,
            self.box_input_last,
        )

    ####################################################################
    # Button callback functions

    async def goto_box_exercise_handler(self, widget: toga.Widget) -> None:
        """Go to foreign exercise page box, button handler."""
        raise NotImplementedError(
            'Subclasses must provide a goto_exercise_box_handler() method.'
        )

    def save_params_handler(self, widget: toga.Widget) -> None:
        """Save Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        raise NotImplementedError(
            'Subclasses must provide a save_params_handler() method.'
        )

    ####################################################################
    # Switch callback functions

    def first_switch_handler(self, widget: toga.Widget) -> None:
        """Count of first added words, switch handler."""
        if self.count_first_switch.value:
            self.count_last_switch.value = False

    def last_switch_handler(self, widget: toga.Widget) -> None:
        """Count of last added words, switch handler."""
        if self.count_last_switch.value:
            self.count_first_switch.value = False

    ####################################################################
    # Lookup conditions

    @property
    def lookup_conditions(self) -> dict[str, str | list | None]:
        """User lookup conditions (`dict`, reade-only).

        Sets the data in the selection widgets to display.
        Gets the data from the selection widgets to request
        a task from the server.
        """
        # NumberInput return Decimal objects or None.
        count_first = int(self.input_count_first.value or 0)
        count_last = int(self.input_count_last.value or 0)
        lookup_conditions = {
            PERIOD_START: self.selection_start_period.get_alias(),
            PERIOD_END: self.selection_end_period.get_alias(),
            CATEGORY: self.selection_category.get_alias(),
            PROGRESS: self.selection_progress.get_alias(),
            'count_first': count_first * self.count_first_switch.value,
            'count_last': count_last * self.count_last_switch.value,
        }
        return lookup_conditions

    @lookup_conditions.setter
    def lookup_conditions(self, value: list[dict]) -> None:
        # Initial values for the selection.
        defaults = value[LOOKUP_CONDITIONS]
        # Items to display for selection.
        items = value[EXERCISE_CHOICES]

        self.selection_start_period.set_items(
            items[EDGE_PERIODS], defaults[PERIOD_START]
        )
        self.selection_end_period.set_items(
            items[EDGE_PERIODS], defaults[PERIOD_END]
        )
        self.selection_category.set_items(
            items[CATEGORIES], defaults[CATEGORY]
        )
        self.selection_progress.set_items(
            items[PROGRESS], defaults[PROGRESS]
        )  # fmt: skip
        if bool(defaults['count_first']):
            self.input_count_first.value = defaults['count_first']
            self.count_first_switch.value = True
            self.count_last_switch.value = False
        if bool(defaults['count_last']):
            self.input_count_last.value = defaults['count_last']
            self.count_last_switch.value = True
            self.count_first_switch.value = False


class ExerciseBox(BoxApp):
    """Exercise box of widgets."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__(style=Pack(direction=COLUMN))
        # The box has event timing control.
        self.timer = Timer()
        # The box has task control.
        self.task = Task()
        # To override attrs.
        self.url_exercise = ''
        self.url_progress = ''

        # Style.
        label_style = Pack(padding=(0, 0, 0, 7))

        # Inner boxes.
        self.box_exercise = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
            )
        )
        box_btn_group = toga.Box(
            style=Pack(
                direction=ROW,
                height=100,
            )
        )

        # Text display widgets.
        self.question_display = TextPanel()
        self.answer_display = TextPanel()
        self.question_display.style.flex = 2
        self.answer_display.style.flex = 2

        # Widgets DOM.
        self.box_exercise.add(
            toga.Label('Вопрос:', style=label_style),
            self.question_display,
            toga.Label('Ответ:', style=label_style),
            self.answer_display,
            box_btn_group,
        )
        box_btn_group.add(
            AnswerBtn('Пауза', self.pause_handler),
            AnswerBtn('Не знаю', self.not_know_handler),
            AnswerBtn('Знаю', self.know_handler),
            AnswerBtn('Далее', self.next_handler),
        )

    ####################################################################
    # Button handlers

    async def know_handler(self, _: toga.Widget) -> None:
        """Mark that know the answer, button handler."""
        know_payload = {ACTION: KNOW, ITEM_ID: self.task.item_id}
        await request_post_async(self.url_progress, know_payload)
        await self.move_to_next_task()

    async def not_know_handler(self, _: toga.Widget) -> None:
        """Mark that not know the answer, button handler."""
        not_know_payload = {ACTION: NOT_KNOW, ITEM_ID: self.task.item_id}
        await request_post_async(self.url_progress, not_know_payload)
        await self.move_to_next_task()

    async def move_to_next_task(self) -> None:
        """Move to next task."""
        self.task.status = QUESTION
        await self.loop_task()

    def pause_handler(self, _: toga.Widget) -> None:
        """Exercise pause, button handler."""
        self.timer.on_pause()

    async def next_handler(self, _: toga.Widget) -> None:
        """Switch to the next task, button handler."""
        self.timer.unpause()
        await self.loop_task()

    # End Button handlers
    #####################

    async def request_task(self) -> None:
        """Request the task data."""
        r = request_post(self.url_exercise, self.task.params)
        if r.status_code == HTTPStatus.OK:
            self.task.data = r.json()
            return
        elif r.status_code == HTTPStatus.NO_CONTENT:
            await self.show_message('', NO_TASK_MSG)
            self.move_to_box_params(self)
        else:
            await self.show_message('', TASK_ERROR_MSG)
        self.task.data = None

    def show_question(self) -> None:
        """Show the task question without an answer."""
        self.question_display.update(self.task.question)
        self.answer_display.clean()

    def show_answer(self) -> None:
        """Show the task answer."""
        self.answer_display.update(self.task.answer)

    async def loop_task(self) -> None:
        """Show new task in loop."""
        self.timer.cancel()

        while self.is_enable_new_task():
            if self.task.status != ANSWER:
                self.clean_text_panel()
                await self.request_task()
                if not self.task.data:
                    break
                self.show_question()
                self.task.status = ANSWER
            else:
                self.show_answer()
                self.task.status = QUESTION
            await self.timer.start()

    def is_enable_new_task(self) -> bool:
        """Return `False` to cancel task update, `True` otherwise."""
        if not self.timer.is_pause():
            return self.is_visible_box(self)
        return False

    def is_visible_box(self, widget: toga.Box) -> bool:
        """Is the box of widget is main_window content."""
        return bool(widget.root.app.main_window.content == self)

    def clean_text_panel(self) -> None:
        """Clean the test panel."""
        self.answer_display.clean()
        self.question_display.clean()

    def move_to_box_params(self, widget: toga.Widget) -> None:
        """Move to exercise parameters page box.

        Override this method.
        """
        pass

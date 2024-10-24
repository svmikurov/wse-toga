"""Container for choice exercise progress parameter.

For exercises:
    * Glossary term study exercise
    * Foreign word study exercise
"""

import toga
from toga.style.pack import COLUMN, ROW, Pack

from wse.constants import (
    ACTION,
    ANSWER,
    CATEGORIES,
    CATEGORY,
    EDGE_PERIODS,
    EXERCISE_CHOICES,
    FOREIGN_EXERCISE_PATH,
    ID,
    KNOW,
    LOOKUP_CONDITIONS,
    NOT_KNOW,
    PERIOD_END,
    PERIOD_START,
    PROGRESS,
    QUESTION,
)
from wse.contrib.http_requests import request_post_async
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
        label_style = Pack(padding=(7, 0, 7, 20))

        # General buttons.
        btn_save_params = BtnApp(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )
        btn_goto_foreign_exercise = BtnApp(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )

        # Selection labels.
        label_start = toga.Label('Начало периода:', style=label_style)
        label_end = toga.Label('Конец периода:', style=label_style)
        label_category = toga.Label('Категория:', style=label_style)
        label_progres = toga.Label('Стадия изучения:', style=label_style)
        # Selections.
        self.start_period_selection = BaseSelection()
        self.end_period_selection = BaseSelection()
        self.category_selection = BaseSelection()
        self.progress_selection = BaseSelection()
        # Selection boxes.
        selection_box_style = Pack(padding=(2, 0, 2, 0))
        selection_start_box = toga.Box(
            style=selection_box_style,
            children=[
                FlexBox(children=[label_start]),
                FlexBox(children=[self.start_period_selection]),
            ],
        )
        selection_start_box.style.padding_top = 4
        selection_end_box = toga.Box(
            style=selection_box_style,
            children=[
                FlexBox(children=[label_end]),
                FlexBox(children=[self.end_period_selection]),
            ],
        )
        selection_category_box = toga.Box(
            style=selection_box_style,
            children=[
                FlexBox(children=[label_category]),
                FlexBox(children=[self.category_selection]),
            ],
        )
        selection_progress_box = toga.Box(
            style=selection_box_style,
            children=[
                FlexBox(children=[label_progres]),
                FlexBox(children=[self.progress_selection]),
            ],
        )

        # Widgets DOM.
        # Add ``params_box`` attr.
        param_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.add(
            TitleLabel(text=self.title),
            param_box,
            btn_goto_foreign_exercise,
            btn_save_params,
        )
        param_box.add(
            selection_start_box,
            selection_end_box,
            selection_category_box,
            selection_progress_box,
        )

    ####################################################################
    # Button callback functions

    async def goto_exercise_box_handler(self, widget: toga.Widget) -> None:
        """Go to foreign exercise page box, button handler."""
        raise NotImplementedError(
            'Subclasses must provide a goto_exercise_box_handler() method.'
        )

    def save_params_handler(self, widget: toga.Widget) -> None:
        """Save Foreign Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        raise NotImplementedError(
            'Subclasses must provide a save_params_handler() method.'
        )

    ####################################################################
    # Lookup conditions

    @property
    def lookup_conditions(self) -> dict[str, str | list | None]:
        """User lookup conditions (`dict`, reade-only).

        Sets the data in the selection widgets to display.
        Gets the data from the selection widgets to request
        a task from the server.
        """
        lookup_conditions = {
            PERIOD_START: self.start_period_selection.get_alias(),
            PERIOD_END: self.end_period_selection.get_alias(),
            CATEGORY: self.category_selection.get_alias(),
            PROGRESS: self.progress_selection.get_alias(),
        }
        return lookup_conditions

    @lookup_conditions.setter
    def lookup_conditions(self, value: list[dict]) -> None:
        # Initial values for the selection.
        defaults = value[LOOKUP_CONDITIONS]
        # Items to display for selection.
        items = value[EXERCISE_CHOICES]

        self.start_period_selection.set_items(
            items[EDGE_PERIODS], defaults[PERIOD_START]
        )
        self.end_period_selection.set_items(
            items[EDGE_PERIODS], defaults[PERIOD_END]
        )
        self.category_selection.set_items(
            items[CATEGORIES], defaults[CATEGORY]
        )
        self.progress_selection.set_items(
            items[PROGRESS], defaults[PROGRESS]
        )  # fmt: skip


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
        self.url_exercise = FOREIGN_EXERCISE_PATH
        self.url_progress = ''

        # Style.
        label_style = Pack(padding=(2, 0, 2, 7))

        # Inner boxes.
        self.exercise_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
            )
        )
        btn_group_box = toga.Box(
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
        self.exercise_box.add(
            toga.Label('Вопрос:', style=label_style),
            self.question_display,
            toga.Label('Ответ:', style=label_style),
            self.answer_display,
            btn_group_box,
        )
        btn_group_box.add(
            AnswerBtn('Пауза', self.pause_handler),
            AnswerBtn('Не знаю', self.not_know_handler),
            AnswerBtn('Знаю', self.know_handler),
            AnswerBtn('Далее', self.next_handler),
        )

    ####################################################################
    # Button handlers

    async def know_handler(self, _: toga.Widget) -> None:
        """Mark that know the answer, button handler."""
        know_payload = {ACTION: KNOW, ID: self.task.item_id}
        await request_post_async(self.url_progress, know_payload)
        await self.loop_task()

    async def not_know_handler(self, _: toga.Widget) -> None:
        """Mark that not know the answer, button handler."""
        not_know_payload = {ACTION: NOT_KNOW, ID: self.task.item_id}
        await request_post_async(self.url_progress, not_know_payload)
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
        r = await request_post_async(self.url_exercise, self.task.params)
        self.task.data = r.json()

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
                await self.request_task()
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

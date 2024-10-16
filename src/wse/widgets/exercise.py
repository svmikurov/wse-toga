"""General exercise box widgets."""

import toga
from toga.style.pack import COLUMN, ROW, Pack

from wse.boxes import base
from wse.boxes.base import BaseBox
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
from wse.widgets.base import (
    BtnApp,
    BaseSelection,
    TextDisplay,
)


class ExerciseParamsSelectionsBox(BaseBox):
    """Exercise param box of selection widgets.

    Use the ``params_box`` attribute of that class to
    add box with selections to widgets DOM of subclass.

    .. code-block:: python
       :caption: For example:

        self.add(
            ...
            self.params_box,
            ...
        )
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.style.update(direction=COLUMN)

        # Styles.
        label_style = Pack(padding=(7, 0, 7, 20))

        # Selection widgets.
        self.start_period_selection = BaseSelection()
        self.end_period_selection = BaseSelection()
        self.progress_selection = BaseSelection()
        self.category_selection = BaseSelection()

        # Inner boxes.
        box_left = toga.Box(style=Pack(flex=1, direction=COLUMN))
        box_right = toga.Box(style=Pack(flex=1, direction=COLUMN))

        # Widgets DOM.
        # Add ``params_box`` attr.
        self.params_box = toga.Box(
            style=Pack(direction=COLUMN),
            children=[toga.Box(children=[box_left, box_right])],
        )
        box_left.add(
            toga.Label('Начало периода:', style=label_style),
            toga.Label('Конец периода:', style=label_style),
            toga.Label('Категория:', style=label_style),
            toga.Label('Стадия изучения:', style=label_style),
        )
        box_right.add(
            self.start_period_selection,
            self.end_period_selection,
            self.category_selection,
            self.progress_selection,
        )

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


class ExerciseBox(base.BaseBox):
    """Exercise box of widgets."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__(style=Pack(direction=COLUMN))
        # The box has event timing control.
        self.timer = Timer()
        # The box has task display control.
        self.task = Task()
        # To override attrs.
        self.url_exercise = FOREIGN_EXERCISE_PATH
        self.url_progress = ''

        # Style.
        label_style = Pack(padding=(10, 0, 10, 20))

        # Inner boxes.
        self.exercise_box = toga.Box(style=Pack(direction=COLUMN))
        btn_group_box = toga.Box(style=Pack(direction=ROW))

        # Text display widgets.
        self.question_display = TextDisplay()
        self.answer_display = TextDisplay()

        # Widgets DOM.
        self.exercise_box.add(
            toga.Label('Вопрос:', style=label_style),
            self.question_display,
            toga.Label('Ответ:', style=label_style),
            self.answer_display,
            btn_group_box,
        )
        btn_group_box.add(
            BtnApp('Не знаю', self.not_know_handler),
            BtnApp('Знаю', self.know_handler),
            BtnApp('Пауза', self.pause_handler),
            BtnApp('Далее', self.next_handler),
        )

    ####################################################################
    # Button handlers

    async def know_handler(self, _: toga.Button) -> None:
        """Mark that know the answer, button handler."""
        know_payload = {ACTION: KNOW, ID: self.task.item_id}
        await request_post_async(self.url_progress, know_payload)
        await self.loop_task()

    async def not_know_handler(self, _: toga.Button) -> None:
        """Mark that not know the answer, button handler."""
        not_know_payload = {ACTION: NOT_KNOW, ID: self.task.item_id}
        await request_post_async(self.url_progress, not_know_payload)
        await self.loop_task()

    def pause_handler(self, _: toga.Button) -> None:
        """Exercise pause, button handler."""
        self.timer.on_pause()

    async def next_handler(self, _: toga.Button) -> None:
        """Switch to the next task, button handler."""
        self.timer.unpause()
        await self.loop_task()

    # End Button handlers
    #####################

    async def request_task(self) -> None:
        """Request the task data."""
        r = await request_post_async(self.url_exercise, self.task.params)
        self.task.data = r.json()
        print(f'{self.task.params = }')

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

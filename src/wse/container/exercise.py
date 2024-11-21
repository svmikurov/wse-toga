"""Container for choice exercise progress parameter.

For exercises:
    * Glossary term study exercise
    * Foreign word study exercise
"""

from http import HTTPStatus

import toga
from toga.style.pack import COLUMN, ROW, Pack

from wse.constants import (
    NO_TASK_MSG,
    TASK_ERROR_MSG,
)
from wse.contrib.http_requests import (
    HttpPutMixin,
    request_get,
    request_post,
    request_post_async,
)
from wse.contrib.task import Task
from wse.contrib.timer import Timer
from wse.handlers.goto_handler import set_window_content
from wse.widgets.box import FlexBox
from wse.widgets.box_page import BoxApp
from wse.widgets.button import BtnApp
from wse.widgets.label import TitleLabel
from wse.widgets.selection import BaseSelection
from wse.widgets.text_input import TextPanel


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


class ExerciseParamSelectionsBox(HttpPutMixin, BoxApp):
    """Exercise param box of selection widgets."""

    title = ''
    """Page box title (`str`).
    """
    url = ''
    """Learning foreign word exercise parameters url (`str`).
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

    async def on_open(self, widget: toga.Widget) -> None:
        """Request and fill params data of box when box open."""
        response = request_get(url=self.url)
        if response.status_code == HTTPStatus.OK:
            self.lookup_conditions = response.json()

    ####################################################################
    # Button callback functions

    async def goto_box_exercise_handler(self, widget: toga.Widget) -> None:
        """Go to foreign exercise page box, button handler."""
        raise NotImplementedError(
            'Subclasses must provide a goto_exercise_box_handler() method.'
        )

    async def save_params_handler(self, _: toga.Widget) -> None:
        """Request to save foreign exercise params, button handler."""
        payload = self.lookup_conditions
        await self.request_put_async(self.url, payload)

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
            'period_start_date': self.selection_start_period.get_alias(),
            'period_end_date': self.selection_end_period.get_alias(),
            'category': self.selection_category.get_alias(),
            'progress': [self.selection_progress.get_alias()],
            'count_first': count_first * self.count_first_switch.value,
            'count_last': count_last * self.count_last_switch.value,
        }
        return lookup_conditions

    @lookup_conditions.setter
    def lookup_conditions(self, value: dict) -> None:
        # Initial values for the selection.
        defaults = value['lookup_conditions']
        # Items to display for selection.
        items = value['exercise_choices']

        self.selection_start_period.set_items(
            items['edge_period_items'], defaults['period_start_date']
        )
        self.selection_end_period.set_items(
            items['edge_period_items'], defaults['period_end_date']
        )
        self.selection_category.set_items(
            items['categories'], defaults['category']
        )
        self.selection_progress.set_items(
            items['progress'], defaults['progress']
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
    """Exercise container of widgets."""

    title = ''
    """The box-container title (`str`).
    """

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
        self.label_question = toga.Label('Вопрос:', style=label_style)
        self.label_answer = toga.Label('Ответ:', style=label_style)

        self.label_title = TitleLabel(self.title)

        self.btn_pause = AnswerBtn('Пауза', self.pause_handler)
        self.btn_not_know = AnswerBtn('Не знаю', self.not_know_handler)
        self.btn_know = AnswerBtn('Знаю', self.know_handler)
        self.btn_next = AnswerBtn('Далее', self.next_handler)

        # Inner boxes.
        self.box_exercise = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
            )
        )
        self.box_btn_group = toga.Box(
            style=Pack(
                direction=ROW,
                height=100,
            )
        )

        # Text display widgets.
        self.text_panel_question = TextPanel()
        self.text_panel_answer = TextPanel()
        self.text_panel_question.style.flex = 2
        self.text_panel_answer.style.flex = 2

        # Widgets DOM.
        self.box_exercise.add(
            self.label_question,
            self.text_panel_question,
            self.label_answer,
            self.text_panel_answer,
            self.box_btn_group,
        )
        self.box_btn_group.add(
            self.btn_pause,
            self.btn_not_know,
            self.btn_know,
            self.btn_next,
        )

    async def on_open(self, widget: toga.Widget) -> None:
        """Start exercise."""
        self.set_params()
        self.clean_text_panel()
        self.reset_task_status()
        await self.loop_task()

    ####################################################################
    # Button handlers

    async def know_handler(self, _: toga.Widget) -> None:
        """Mark that know the answer, button handler."""
        know_payload = {'action': 'know', 'item_id': self.task.item_id}
        await request_post_async(self.url_progress, know_payload)
        await self.move_to_next_task()

    async def not_know_handler(self, _: toga.Widget) -> None:
        """Mark that not know the answer, button handler."""
        not_know_payload = {'action': 'not_know', 'item_id': self.task.item_id}
        await request_post_async(self.url_progress, not_know_payload)
        await self.move_to_next_task()

    async def move_to_next_task(self) -> None:
        """Move to next task."""
        self.task.status = 'question'
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

    def set_params(self) -> None:
        """Set exercise params to exercise attr."""
        box_params = self.get_box_params()
        self.task.params = box_params.lookup_conditions

    async def request_task(self) -> None:
        """Request the task data."""
        response = request_post(self.url_exercise, self.task.params)
        if response.status_code == HTTPStatus.OK:
            self.task.data = response.json()
            return
        elif response.status_code == HTTPStatus.NO_CONTENT:
            await self.show_message('', NO_TASK_MSG)
            await self.move_to_box_params(self)
        else:
            await self.show_message('', TASK_ERROR_MSG)
        self.task.data = None

    def show_question(self) -> None:
        """Show the task question without an answer."""
        self.text_panel_question.update(self.task.question)
        self.text_panel_answer.clean()

    def show_answer(self) -> None:
        """Show the task answer."""
        self.text_panel_answer.update(self.task.answer)

    async def loop_task(self) -> None:
        """Show new task in loop."""
        self.timer.cancel()

        while self.is_enable_new_task():
            if self.task.status != 'answer':
                self.clean_text_panel()
                await self.request_task()
                if not self.task.data:
                    break
                self.show_question()
                self.task.status = 'answer'
            else:
                self.show_answer()
                self.task.status = 'question'
            await self.timer.start()

    def reset_task_status(self) -> None:
        """Reset the task status."""
        self.task.status = None

    def is_enable_new_task(self) -> bool:
        """Return `False` to cancel task update, `True` otherwise."""
        if not self.timer.is_pause():
            return self.is_visible_box(self)
        return False

    def is_visible_box(self, widget: toga.Box) -> bool:
        """Is the box of widget is main_window content."""
        return widget.root.app.main_window.content == self

    def clean_text_panel(self) -> None:
        """Clean the test panel."""
        self.text_panel_answer.clean()
        self.text_panel_question.clean()

    async def move_to_box_params(self, widget: toga.Widget) -> None:
        """Move to exercise parameters page box.

        Override this method.
        """
        box = self.get_box_params()
        await set_window_content(self, box)

    def get_box_params(self) -> ExerciseParamSelectionsBox:
        """Get box instance with exercise params.

        Override this method.
        """
        raise NotImplementedError(
            'Subclasses must provide a box_name_params method.'
        )

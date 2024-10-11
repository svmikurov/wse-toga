"""English box."""

import asyncio
from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response
from toga.style import Pack
from travertino.constants import COLUMN, ROW

from wse import base
from wse.constants import (
    ACTION,
    ALIAS,
    ANSWER,
    ANSWER_TEXT,
    CATEGORIES,
    CATEGORY,
    DEFAULT_TIMEOUT,
    DETAIL,
    EDGE_PERIOD_ITEMS,
    ERROR,
    EXERCISE_CHOICES,
    FOREIGN_BOX,
    FOREIGN_EXERCISE_BOX,
    FOREIGN_EXERCISE_PATH,
    FOREIGN_PARAMS_BOX,
    FOREIGN_PARAMS_PATH,
    FOREIGN_PROGRESS_PATH,
    HOST_API,
    HUMANLY,
    ID,
    KNOW,
    LOOKUP_CONDITIONS,
    MAIN_BOX,
    NAME,
    NOT_KNOW,
    PERIOD_END,
    PERIOD_START,
    PROGRESS,
    QUESTION,
    QUESTION_TEXT,
)
from wse.http_requests import (
    app_auth,
    request_get,
    request_post,
    request_post_async,
)
from wse.tools import set_selection_item


class ForeignBox(base.BaseBox):
    """Learning foreign words main box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = base.BaseButton(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        btn_goto_params_box = base.BaseButton(
            'Упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_params_box,
        )


class ForeignParamsBox(base.BaseBox):
    """Learning foreign words exercise parameters box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Styles.
        label_style = Pack(padding=(7, 0, 7, 20))
        pair_box_style = Pack(flex=1, direction=COLUMN)

        # Box widgets.
        btn_goto_glossary_box = base.BaseButton(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        btn_goto_glossary_exercise_box = base.BaseButton(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )
        btn_save_params = base.BaseButton(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )

        # Parameter widgets.
        # labels
        start_date_label = toga.Label('Начало периода:', style=label_style)
        end_date_label = toga.Label('Конец периода:', style=label_style)
        category_label = toga.Label('Категория:', style=label_style)
        progress_label = toga.Label('Стадия изучения:', style=label_style)
        # selections
        self.start_period_selection = toga.Selection(accessor=HUMANLY)
        self.end_period_selection = toga.Selection(accessor=HUMANLY)
        self.category_selection = toga.Selection(accessor=NAME)
        self.progress_selection = toga.Selection(accessor=HUMANLY)
        # boxes
        box_pair = toga.Box()
        box_left = toga.Box(style=pair_box_style)
        box_right = toga.Box(style=pair_box_style)

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            btn_save_params,
            box_pair,
            btn_goto_glossary_exercise_box,
        )
        box_pair.add(box_left, box_right)
        box_left.add(
            start_date_label,
            end_date_label,
            category_label,
            progress_label,
        )
        box_right.add(
            self.start_period_selection,
            self.end_period_selection,
            self.category_selection,
            self.progress_selection,
        )

    @property
    def lookup_conditions(self) -> dict[str, str | list]:
        """User lookup conditions (`dict`, reade-only)."""
        # selection.value is None if not is set
        period_start = self.start_period_selection.value
        period_end = self.end_period_selection.value
        category = self.category_selection.value
        progres = self.progress_selection.value
        lookup_conditions = {
            PERIOD_START: period_start.alias if period_start else None,
            PERIOD_END: period_end.alias if period_end else None,
            CATEGORY: category.id if category else None,
            PROGRESS: progres.alias if progres else None,
        }
        return lookup_conditions

    async def goto_exercise_box_handler(self, widget: toga.Button) -> None:
        """Go to glossary exercise, button handler."""
        exercise_box = self.get_box(widget, FOREIGN_EXERCISE_BOX)
        try:
            exercise_box.lookup_conditions = self.lookup_conditions
        except AttributeError as error:
            await self.show_message('', 'Войдите в учетную запись')
            raise error
        else:
            self.set_window_content(widget, exercise_box)
            await exercise_box.show_task()

    def on_open(self) -> None:
        """Request and fill params data."""
        url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
        response = request_get(url=url, auth=app_auth)
        self.fill_params(response)

    def save_params_handler(self, _: toga.Button) -> None:
        """Save Glossary Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
        request_post(url, self.lookup_conditions, app_auth)

    def fill_params(self, response: Response) -> None:
        """Fill Glossary Exercise parameters.

        Parameters
        ----------
        response : `httpx.Response`
            Server response with choices and current exercise parameters
            as choice by default.

        """
        if response.status_code == HTTPStatus.OK:
            payload = response.json()
            exercise_choices = payload[EXERCISE_CHOICES]

            # Choices.
            edge_period_items = exercise_choices[EDGE_PERIOD_ITEMS]
            category_items = exercise_choices[CATEGORIES]
            progress_items = exercise_choices[PROGRESS]

            # Default choice.
            defaults = payload[LOOKUP_CONDITIONS]
            start_period_alias = defaults[PERIOD_START]
            end_period_alias = defaults[PERIOD_END]
            default_category = defaults[CATEGORY]
            default_progress = defaults[PROGRESS]

            # Assign the choices to selection.
            self.start_period_selection.items = edge_period_items
            self.end_period_selection.items = edge_period_items
            self.category_selection.items = category_items
            self.progress_selection.items = progress_items

            # Assign the default choice to selection.
            set_selection_item(
                key=ALIAS,
                value=start_period_alias,
                items=edge_period_items,
                selection=self.start_period_selection,
            )
            set_selection_item(
                key=ALIAS,
                value=end_period_alias,
                items=edge_period_items,
                selection=self.end_period_selection,
            )
            set_selection_item(
                key=ID,
                value=default_category,
                items=category_items,
                selection=self.category_selection,
            )
            set_selection_item(
                key=ALIAS,
                value=default_progress,
                items=progress_items,
                selection=self.progress_selection,
            )


class ForeignExerciseBox(base.BaseBox):
    """English exercise box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.auth = app_auth
        self.url_exercise = urljoin(HOST_API, FOREIGN_EXERCISE_PATH)
        self.url_progress = urljoin(HOST_API, FOREIGN_PROGRESS_PATH)
        self.word_id: int | None = None
        self.coro_task_timer = None
        self.pause = False
        self.timeout = DEFAULT_TIMEOUT
        self.task_status = None
        self.task_data = None
        self.lookup_conditions = None

        # Common styles.
        text_style = Pack(padding=(0, 5, 0, 5))
        label_style = Pack(padding=(10, 0, 10, 20))
        bottom_group_btn_style = Pack(flex=1, height=60)

        # Buttons.
        btn_goto_glossary_box = base.BaseButton(
            'Англо-Русский словарь',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        btn_goto_glossary_exercise_parameters_box = base.BaseButton(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )
        # Bottom group buttons.
        btn_not_know = toga.Button(
            'Не знаю',
            on_press=self.btn_not_know_handler,
            style=bottom_group_btn_style,
        )
        btn_know = toga.Button(
            'Знаю',
            on_press=self.btn_know_handler,
            style=bottom_group_btn_style,
        )
        btn_pause = toga.Button(
            'Пауза',
            on_press=self.pause_handler,
            style=bottom_group_btn_style,
        )
        btn_next = toga.Button(
            'Далее',
            on_press=self.btn_next_handler,
            style=bottom_group_btn_style,
        )

        # Box widgets.
        question_label = toga.Label(
            text='Вопрос:',
            style=label_style,
        )
        self.question = toga.MultilineTextInput(
            readonly=True,
            style=text_style,
        )
        answer_label = toga.Label(
            text='Ответ:',
            style=label_style,
        )
        self.answer = toga.MultilineTextInput(
            readonly=True,
            style=text_style,
        )
        bottom_group_box = toga.Box(
            style=Pack(direction=ROW),
        )

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            btn_goto_glossary_exercise_parameters_box,
            question_label,
            self.question,
            answer_label,
            self.answer,
            bottom_group_box,
        )
        bottom_group_box.add(
            btn_pause,
            btn_not_know,
            btn_know,
            btn_next,
        )

    async def btn_know_handler(self, _: toga.Button) -> None:
        """Mark that know the answer, button handler."""
        payload = {
            ACTION: KNOW,
            ID: self.word_id,
        }
        await request_post_async(self.url_progress, payload=payload)
        await self.show_task()

    async def btn_not_know_handler(self, _: toga.Button) -> None:
        """Mark that not know the answer, button handler."""
        payload = {
            ACTION: NOT_KNOW,
            ID: self.word_id,
        }
        await request_post_async(self.url_progress, payload=payload)
        await self.show_task()

    def pause_handler(self, _: toga.Button) -> None:
        """Exercise pause, button handler."""
        self.pause = False if self.pause else True

    async def btn_next_handler(self, _: toga.Button) -> None:
        """Switch to the next task, button handler."""
        self.pause = False
        await self.show_task()

    @property
    def is_enable_new_task(self) -> bool:
        """Return `False` to cancel task update, `True` otherwise."""
        if not self.pause:
            return self.is_visible_box(self)
        return False

    def is_visible_box(self, widget: toga.Box) -> bool:
        """Is the box of widget is main_window content."""
        return widget.root.app.main_window.content == self

    async def show_task(self) -> None:
        """Show new task."""
        if self.coro_task_timer:
            self.coro_task_timer.cancel()

        while self.is_enable_new_task:
            if self.task_status != ANSWER:
                response = await request_post_async(
                    self.url_exercise,
                    self.lookup_conditions,
                )
                self.task_data = response.json()

                if response.status_code != HTTPStatus.OK:
                    msg = 'Необработанная ошибка'
                    if DETAIL in self.task_data:
                        msg = self.task_data.get(DETAIL)
                    elif ERROR in self.task_data:
                        msg = self.task_data.get(ERROR)
                    await self.show_message('Сообщение:', msg)
                    break

                self.word_id = self.task_data[ID]
                self.question.value = self.task_data[QUESTION_TEXT]
                self.answer.value = None
                self.task_status = ANSWER
            else:
                self.question.value = self.task_data[QUESTION_TEXT]
                self.answer.value = self.task_data[ANSWER_TEXT]
                self.task_status = QUESTION

            self.coro_task_timer = asyncio.create_task(
                asyncio.sleep(self.timeout)
            )
            await self.coro_task_timer

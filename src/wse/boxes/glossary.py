"""Glossary page boxes."""

import asyncio
from http import HTTPStatus
from urllib.parse import urljoin

import toga
from toga.style import Pack
from travertino.constants import ROW

from wse import base
from wse.boxes.widgets.exercise import ExerciseParamChoicesBox
from wse.constants import (
    ACTION,
    ANSWER,
    ANSWER_TEXT,
    DEFAULT_TIMEOUT,
    DETAIL,
    ERROR,
    GLOS_BOX,
    GLOS_EXE_BOX,
    GLOS_EXE_PATH,
    GLOS_PARAMS_BOX,
    GLOS_PARAMS_PATH,
    GLOS_PROGRESS,
    HOST_API,
    ID,
    KNOW,
    MAIN_BOX,
    NOT_KNOW,
    QUESTION,
    QUESTION_TEXT,
)
from wse.http_requests import (
    app_auth,
    request_get,
    request_post,
    request_post_async,
)


class GlossaryBox(base.BaseBox):
    """Glossary box."""

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
            on_press=lambda _: self.goto_box_handler(_, GLOS_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_params_box,
        )


class GlossaryParamsBox(base.BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_glossary_box = base.BaseButton(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, GLOS_BOX),
        )
        btn_goto_glossary_exercise_box = base.BaseButton(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )
        btn_save_params = base.BaseButton(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )
        self.params_box = ExerciseParamChoicesBox()

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            self.params_box,
            btn_save_params,
            btn_goto_glossary_exercise_box,
        )

    async def goto_exercise_box_handler(self, widget: toga.Button) -> None:
        """Go to glossary exercise, button handler."""
        exercise_box = self.get_box(widget, GLOS_EXE_BOX)
        try:
            exercise_box.lookup_conditions = self.params_box.lookup_conditions
        except AttributeError as error:
            await self.show_message('', 'Войдите в учетную запись')
            raise error
        else:
            self.set_window_content(widget, exercise_box)
            await exercise_box.show_task()

    def on_open(self) -> None:
        """Request and fill params data."""
        url = urljoin(HOST_API, GLOS_PARAMS_PATH)
        response = request_get(url=url, auth=app_auth)
        self.params_box.fill_params(response)

    def save_params_handler(self, _: toga.Button) -> None:
        """Save Glossary Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(HOST_API, GLOS_PARAMS_PATH)
        request_post(url, self.params_box.lookup_conditions)


class GlossaryExerciseBox(base.BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.auth = app_auth
        self.url_exercise = urljoin(HOST_API, GLOS_EXE_PATH)
        self.url_progress = urljoin(HOST_API, GLOS_PROGRESS)
        self.term_id: int | None = None
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
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, GLOS_BOX),
        )
        btn_goto_glossary_exercise_parameters_box = base.BaseButton(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, GLOS_PARAMS_BOX),
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
            ID: self.term_id,
        }
        await request_post_async(self.url_progress, payload=payload)
        await self.show_task()

    async def btn_not_know_handler(self, _: toga.Button) -> None:
        """Mark that not know the answer, button handler."""
        payload = {
            ACTION: NOT_KNOW,
            ID: self.term_id,
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

                self.term_id = self.task_data[ID]
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

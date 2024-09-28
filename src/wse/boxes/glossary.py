"""Glossary box."""

import asyncio
from urllib.parse import urljoin

import httpx
import toga
from httpx import Response
from toga.style import Pack
from travertino.constants import COLUMN, ROW

from wse import base
from wse import constants as const
from wse.http_requests import app_auth, send_get_request, send_post_request
from wse.tools import set_selection_item


class GlossaryBox(base.BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = base.BaseButton(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )
        btn_goto_params_box = base.BaseButton(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, const.GLOS_PARAMS_BOX),
        )
        btn_goto_exercise_box = base.BaseButton(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_params_box,
            btn_goto_exercise_box,
        )

    async def goto_exercise_box_handler(self, widget: toga.Button) -> None:
        """Go to glossary exercise, button handler."""
        box = self.get_box(widget, const.GLOS_EXE_BOX)
        self.set_window_content(widget, box)
        await box.show_task()


class GlossaryParamsBox(base.BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Styles.
        label_style = Pack(padding=(7, 0, 7, 20))
        pair_box_style = Pack(flex=1, direction=COLUMN)

        # Box widgets.
        btn_goto_glossary_box = base.BaseButton(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, const.GLOS_BOX),
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
        period_label = toga.Label(
            text='Период добавления слова (начало / конец периода):',
            style=label_style,
        )
        self.start_period_selection = toga.Selection(accessor=const.HUMANLY)
        self.end_period_selection = toga.Selection(accessor=const.HUMANLY)

        category_label = toga.Label(text='Категория:', style=label_style)
        category_box_pair = toga.Box()
        category_box_left = toga.Box(style=pair_box_style)
        category_box_right = toga.Box(style=pair_box_style)
        self.category_selection = toga.Selection(accessor=const.NAME)

        progres_label = toga.Label(text='Стадия изучения:', style=label_style)
        progres_box_pair = toga.Box()
        progres_box_left = toga.Box(style=pair_box_style)
        progres_box_right = toga.Box(style=pair_box_style)
        self.progres_selection = toga.Selection(accessor=const.HUMANLY)

        period_box_pair = toga.Box()
        period_box_left = toga.Box(style=pair_box_style)
        period_box_right = toga.Box(style=pair_box_style)

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            btn_save_params,
            period_label,
            period_box_pair,
            category_box_pair,
            progres_box_pair,
            btn_goto_glossary_exercise_box,
        )

        period_box_pair.add(period_box_left, period_box_right)
        period_box_left.add(self.start_period_selection)
        period_box_right.add(self.end_period_selection)

        category_box_pair.add(category_box_left, category_box_right)
        category_box_left.add(category_label)
        category_box_right.add(self.category_selection)

        progres_box_pair.add(progres_box_left, progres_box_right)
        progres_box_left.add(progres_label)
        progres_box_right.add(self.progres_selection)

    async def goto_exercise_box_handler(self, widget: toga.Button) -> None:
        """Go to glossary exercise, button handler."""
        box = self.get_box(widget, const.GLOS_EXE_BOX)
        self.set_window_content(widget, box)
        await box.show_task()

    def on_open(self) -> None:
        """Request and fill params data."""
        url = urljoin(const.HOST_API, const.GLOS_PARAMS_PATH)
        response = send_get_request(url=url, auth=app_auth)
        self.fill_params(response)

    def save_params_handler(self, _: toga.Button) -> None:
        """Save Glossary Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(const.HOST_API, const.GLOS_PARAMS_PATH)
        params = {
            const.PERIOD_START: self.start_period_selection.value.alias,
            const.PERIOD_END: self.end_period_selection.value.alias,
            const.CATEGORY: self.category_selection.value.id,
            const.PROGRES: self.progres_selection.value.alias,
        }
        send_post_request(url=url, payload=params, auth=app_auth)

    def fill_params(self, response: Response) -> None:
        """Fill Glossary Exercise parameters.

        Parameters
        ----------
        response : `httpx.Response`
            Server response with choices and current exercise parameters
            as choice by default.

        """
        if response.status_code == const.HTTP_200_OK:
            payload = response.json()

            # Choices.
            edge_period_items = payload['edge_period_items']
            category_items = payload[const.CATEGORIES]
            progres_items = payload[const.PROGRES]

            # Default choice.
            defaults = payload['parameters']
            start_period_alias = defaults[const.PERIOD_START]
            end_period_alias = defaults[const.PERIOD_END]
            default_cat = defaults[const.CATEGORY]
            default_progres = defaults[const.PROGRES]

            # Assign the choices to selection.
            self.start_period_selection.items = edge_period_items
            self.end_period_selection.items = edge_period_items
            self.category_selection.items = category_items
            self.progres_selection.items = progres_items

            # Assign the default choice to selection.
            set_selection_item(
                key=const.ALIAS,
                value=start_period_alias,
                items=edge_period_items,
                selection=self.start_period_selection,
            )
            set_selection_item(
                key=const.ALIAS,
                value=end_period_alias,
                items=edge_period_items,
                selection=self.end_period_selection,
            )
            set_selection_item(
                key=const.ID,
                value=default_cat,
                items=category_items,
                selection=self.category_selection,
            )
            set_selection_item(
                key=const.ALIAS,
                value=default_progres,
                items=progres_items,
                selection=self.progres_selection,
            )


class GlossaryExerciseBox(
    base.BaseBox,
):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.auth = app_auth
        self.url_exercise = urljoin(const.HOST_API, const.GLOS_EXE_PATH)
        self.url_progres = urljoin(const.HOST_API, const.GLOS_PROGRES)
        self.term_id: int | None = None
        self.coro_task_timer = None
        self.pause = False

        # Common styles.
        text_style = Pack(padding=(0, 5, 0, 5))
        label_style = Pack(padding=(10, 0, 10, 20))
        bottom_group_btn_style = Pack(flex=1, height=60)

        # Buttons.
        btn_goto_glossary_box = base.BaseButton(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, const.GLOS_BOX),
        )
        btn_goto_glossary_exercise_parameters_box = base.BaseButton(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, const.GLOS_PARAMS_BOX),
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
        btn_next = toga.Button(
            'Далее',
            on_press=self.btn_next_handler,
            style=bottom_group_btn_style,
        )
        btn_pause = toga.Button(
            'Пауза',
            on_press=self.pause_handler,
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
            btn_not_know,
            btn_know,
            btn_next,
            btn_pause,
        )

    async def btn_know_handler(self, _: toga.Button) -> None:
        """Mark that know the answer, button handler."""
        payload = {
            const.ACTION: const.KNOW,
            const.ID: self.term_id,
        }
        await self.request_post(payload=payload)
        await self.show_task()

    async def btn_not_know_handler(self, _: toga.Button) -> None:
        """Mark that not know the answer, button handler."""
        payload = {
            const.ACTION: const.NOT_KNOW,
            const.ID: self.term_id,
        }
        await self.request_post(payload=payload)
        await self.show_task()

    async def btn_next_handler(self, _: toga.Button) -> None:
        """Switch to the next task, button handler."""
        self.pause = False
        await self.show_task()

    def pause_handler(self, _: toga.Button) -> None:
        """Exercise pause, button handler."""
        self.pause = False if self.pause else True

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
            response = await self.request_get()
            task_data = response.json()
            self.term_id = task_data[const.ID]
            self.question.value = task_data['question_text']
            self.answer.value = task_data['answer_text']

            self.coro_task_timer = asyncio.create_task(asyncio.sleep(5))
            await self.coro_task_timer

    async def request_get(self) -> Response:
        """Request the next task."""
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.get(self.url_exercise)
        return response

    async def request_post(self, payload: dict) -> Response:
        """Request the progres update."""
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.post(self.url_progres, json=payload)
        return response

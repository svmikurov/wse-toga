"""Foreign words page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response
from toga import MultilineTextInput
from toga.style import Pack

from wse.constants import (
    BTN_GOTO_FOREIGN_CREATE,
    BTN_GOTO_FOREIGN_LIST,
    BTN_GOTO_FOREIGN_MAIN,
    BTN_GOTO_FOREIGN_PARAMS,
    BTN_GOTO_MAIN,
    FOREIGN_ASSESSMENT_PATH,
    FOREIGN_DETAIL_PATH,
    FOREIGN_EXERCISE_PATH,
    FOREIGN_PARAMS_PATH,
    FOREIGN_PATH,
    HOST_API,
    TITLE_FOREIGN_CREATE,
    TITLE_FOREIGN_EXERCISE,
    TITLE_FOREIGN_LIST,
    TITLE_FOREIGN_MAIN,
    TITLE_FOREIGN_PARAMS,
    TITLE_FOREIGN_UPDATE,
)
from wse.container.exercise import ExerciseBox, ExerciseParamSelectionsBox
from wse.contrib.http_requests import (
    request_post_async,
    request_put_async,
)
from wse.handlers.goto_handler import (
    goto_foreign_create_handler,
    goto_foreign_exercise_handler,
    goto_foreign_list_handler,
    goto_foreign_main_handler,
    goto_foreign_params_handler,
    goto_foreign_update_handler,
    goto_main_handler,
)
from wse.source.foreign import Word, WordSource
from wse.widgets.box_page import BoxApp
from wse.widgets.button import BtnApp
from wse.widgets.form import BaseForm
from wse.widgets.label import TitleLabel
from wse.widgets.table import TableApp
from wse.widgets.text_input import TextInputApp


class MainForeignPage(BoxApp):
    """Learning foreign words the main page box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        self.label_title = TitleLabel(TITLE_FOREIGN_MAIN)
        self.btn_goto_main = BtnApp(BTN_GOTO_MAIN, on_press=goto_main_handler)
        self.btn_goto_params = BtnApp(
            BTN_GOTO_FOREIGN_PARAMS, on_press=goto_foreign_params_handler
        )
        self.btn_goto_create = BtnApp(
            BTN_GOTO_FOREIGN_CREATE, on_press=goto_foreign_create_handler
        )
        self.btn_goto_list = BtnApp(
            BTN_GOTO_FOREIGN_LIST, on_press=goto_foreign_list_handler
        )

        # Widget DOM.
        self.add(
            self.label_title,
            self.btn_goto_main,
            self.btn_goto_params,
            self.btn_goto_create,
            self.btn_goto_list,
        )


class ParamForeignPage(ExerciseParamSelectionsBox):
    """Learning foreign words exercise parameters the page box."""

    title = TITLE_FOREIGN_PARAMS
    url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
    """Learning foreign word exercise parameters url (`str`).
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN, on_press=goto_foreign_main_handler
        )

        # Widget DOM.
        self.insert(4, self.btn_goto_foreign_main)

    async def goto_box_exercise_handler(self, widget: toga.Widget) -> None:
        """Go to foreign exercise page box, button handler."""
        await goto_foreign_exercise_handler(widget)


class ExerciseForeignPage(ExerciseBox):
    """Foreign exercise box.

    :ivar box_exercise: The ExerciseBox attr, container with exercise
        widgets.
    """

    title = TITLE_FOREIGN_EXERCISE

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.url_exercise = urljoin(HOST_API, FOREIGN_EXERCISE_PATH)
        self.url_progress = urljoin(HOST_API, FOREIGN_ASSESSMENT_PATH)

        # Buttons.
        self.btn_goto_params = BtnApp(
            'Параметры упражнения', on_press=goto_foreign_params_handler
        )

        # TextPanel
        self.label_textpanel = toga.Label('Информация об упражнении:')
        self.label_textpanel.style = Pack(padding=(0, 0, 0, 7))
        self.display_exercise_info = MultilineTextInput(readonly=True)

        # Widget DOM.
        self.add(
            self.label_title,
            self.box_exercise,
            self.display_exercise_info,
            self.btn_goto_params,
        )
        self.box_exercise.insert(4, self.label_textpanel)
        self.box_exercise.insert(5, self.display_exercise_info)

    def populate_textpanel(self) -> None:
        """Populate the text panel."""
        self.display_exercise_info.value = (
            f'Найдено слов: {self.task.data["item_count"]}\n'
            f'Оценка знания слова: {self.task.data["assessment"]}'
        )

    def show_question(self) -> None:
        """Add population of text panel."""
        super().show_question()
        self.populate_textpanel()

    def get_box_params(self) -> ParamForeignPage:
        """Get box instance with exercise params."""
        return self.root.app.box_foreign_params


class FormForeign(BaseForm):
    """General form to create and update entries, the container."""

    title = ''
    """Page box title (`str`).
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the foreign form."""
        super().__init__(*args, **kwargs)
        self._entry = Word

        self.label_title = TitleLabel(text=self.title)
        self.btn_goto_foreign_list = BtnApp(
            BTN_GOTO_FOREIGN_LIST,
            on_press=goto_foreign_list_handler,
        )
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN,
            on_press=goto_foreign_main_handler,
        )

        # Word data input widgets.
        self.input_native = TextInputApp(placeholder='Слово на русском')
        self.input_native.style.padding_bottom = 1
        self.input_foreign = TextInputApp(placeholder='Слово на иностранном')
        self.btn_submit = BtnApp(
            self.btn_submit_text,
            on_press=self.submit_handler,
        )

        self.add(
            self.label_title,
            self.input_native,
            self.input_foreign,
            self.btn_submit,
            self.btn_goto_foreign_list,
            self.btn_goto_foreign_main,
        )

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        self.input_native.value = self.entry.native_word
        self.input_foreign.value = self.entry.foreign_word

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        print('ffffffffffffffffffffffffffffffffffffffff')
        self.input_native.clean()
        self.input_foreign.clean()

    def focus_to_input_field(self) -> None:
        """Focus to input field."""
        self.input_native.focus()


class CreateWordPage(FormForeign):
    """Add word to foreign dictionary."""

    title = TITLE_FOREIGN_CREATE
    url = urljoin(HOST_API, FOREIGN_PATH)
    btn_submit_text = 'Добавить'
    success_http_status = HTTPStatus.CREATED

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        entry_create = {
            'foreign_word': self.input_foreign.value,
            'native_word': self.input_native.value,
        }
        return entry_create

    @classmethod
    async def request_async(cls, url: str, payload: dict) -> Response:
        """Request to update."""
        return await request_post_async(url, payload)

    async def handle_success(self, widget: toga.Widget) -> None:
        """Go to foreign list page, if success."""
        self.focus_to_input_field()


class UpdateWordPage(FormForeign):
    """Update the foreign word the box."""

    title = TITLE_FOREIGN_UPDATE
    url = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    btn_submit_text = 'Изменить'
    success_http_status = HTTPStatus.OK

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        entry_updated = {
            'id': str(self.entry.id),
            'foreign_word': self.input_foreign.value,
            'native_word': self.input_native.value,
        }
        return entry_updated

    @classmethod
    async def request_async(cls, url: str, payload: dict) -> Response:
        """Request to update."""
        return await request_put_async(url, payload)

    async def handle_success(self, widget: toga.Widget) -> None:
        """Go to foreign list page, if success."""
        await goto_foreign_list_handler(widget)


class ListForeignPage(TableApp):
    """Table of list of foreign words, the page.

    :ivar Button btn_goto_foreign_main: Button go to Foreign Main page.
    """

    source_class = WordSource()
    source_url = urljoin(HOST_API, FOREIGN_PATH)
    source_url_detail = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    headings = ['Иностранный', 'Русский']

    def __init__(self) -> None:
        """Construct the page."""
        super().__init__()

        self.label_title = TitleLabel(TITLE_FOREIGN_LIST)

        # The navigation buttons.
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN,
            on_press=goto_foreign_main_handler,
        )

        # Page widgets DOM.
        self.add(
            self.label_title,
            self.btn_goto_foreign_main,
            self.btns_manage,
            self.table,
            self.btns_paginate,
        )

    async def create_handler(self, widget: toga.Widget) -> None:
        """Go to create the word form, button handler."""
        await goto_foreign_create_handler(widget)

    async def update_handler(self, widget: toga.Widget) -> None:
        """Go to update the word form, button handler."""
        entry = self.table.selection
        box = self.root.app.box_foreign_update
        box.entry = entry
        await goto_foreign_update_handler(widget)

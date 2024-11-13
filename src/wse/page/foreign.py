"""Foreign words page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from toga import MultilineTextInput
from toga.style import Pack

from wse.constants import (
    ASSESSMENT,
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
    FOREIGN_WORD,
    HOST_API,
    RUSSIAN_WORD,
    TITLE_FOREIGN_CREATE,
    TITLE_FOREIGN_EXERCISE,
    TITLE_FOREIGN_LIST,
    TITLE_FOREIGN_MAIN,
    TITLE_FOREIGN_PARAMS,
    TITLE_FOREIGN_UPDATE,
)
from wse.container.exercise import ExerciseBox, ExerciseParamSelectionsBox
from wse.contrib.http_requests import (
    HttpPostMixin,
    HttpPutMixin,
    request_get,
)
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.form import BaseForm
from wse.general.goto_handler import (
    goto_foreign_create,
    goto_foreign_list,
    goto_foreign_main,
    goto_foreign_params,
    goto_main,
)
from wse.general.label import TitleLabel
from wse.general.table import TableApp
from wse.general.text_input import TextInputApp
from wse.source.foreign import Word, WordSource


class MainForeignPage(BoxApp):
    """Learning foreign words the main page box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        self.label_title = TitleLabel(TITLE_FOREIGN_MAIN)
        self.btn_goto_main = BtnApp(BTN_GOTO_MAIN, on_press=goto_main)
        self.btn_goto_params = BtnApp(
            BTN_GOTO_FOREIGN_PARAMS, on_press=goto_foreign_params
        )
        self.btn_goto_create = BtnApp(
            BTN_GOTO_FOREIGN_CREATE, on_press=goto_foreign_create
        )
        self.btn_goto_list = BtnApp(
            BTN_GOTO_FOREIGN_LIST, on_press=goto_foreign_list
        )

        # Widget DOM.
        self.add(
            self.label_title,
            self.btn_goto_main,
            self.btn_goto_params,
            self.btn_goto_create,
            self.btn_goto_list,
        )


class ParamForeignPage(HttpPutMixin, ExerciseParamSelectionsBox):
    """Learning foreign words exercise parameters the page box."""

    title = TITLE_FOREIGN_PARAMS

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN, on_press=goto_foreign_main
        )

        # Widget DOM.
        self.insert(4, self.btn_goto_foreign_main)

    async def goto_box_exercise_handler(self, widget: toga.Widget) -> None:
        """Go to foreign exercise page box, button handler."""
        exercise_box = widget.root.app.box_foreign_exercise
        exercise_box.clean_text_panel()
        exercise_box.task.status = None
        exercise_box.task.params = self.lookup_conditions
        self.set_window_content(widget, exercise_box)
        await exercise_box.loop_task()

    def on_open(self) -> None:
        """Request and fill params data of box when box open."""
        url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
        response = request_get(url=url)
        if response.status_code == HTTPStatus.OK:
            self.lookup_conditions = response.json()

    async def save_params_handler(self, _: toga.Widget) -> None:
        """Save Foreign Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
        await self.request_put_async(url, self.lookup_conditions)


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
            'Параметры упражнения', on_press=goto_foreign_params
        )

        # TextPanel
        self.label_textpanel = toga.Label('Информация об упражнении:')
        self.label_textpanel.style = Pack(padding=(0, 0, 0, 7))
        self.display_exercise_info = MultilineTextInput(
            readonly=True,
        )

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
            f'Оценка знания слова: {self.task.data[ASSESSMENT]}'
        )

    def show_question(self) -> None:
        """Add population of text panel."""
        super().show_question()
        self.populate_textpanel()

    def move_to_box_params(self, widget: toga.Widget) -> None:
        """Move to exercise parameters page box."""
        goto_foreign_params(widget)


class FormForeign(BaseForm):
    """General form to create and update entries, the container."""

    title = 'Добавить слово'
    """Page box title (`str`).
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the foreign form."""
        super().__init__(*args, **kwargs)
        self._entry = Word

        self.label_title = TitleLabel(text=self.title)
        self.btn_goto_foreign_list = BtnApp(
            BTN_GOTO_FOREIGN_LIST,
            on_press=goto_foreign_list,
        )
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN,
            on_press=goto_foreign_main,
        )
        # Word data input widgets.
        self.input_native = TextInputApp(placeholder='Слово на русском')
        self.input_native.style.padding_bottom = 1
        self.input_foreign = TextInputApp(placeholder='Слово на иностранном')
        self.btn_submit = BtnApp(
            self.btn_submit_name,
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
        self.input_native.clean()
        self.input_foreign.clean()

    def focus_to_input_field(self) -> None:
        """Focus to input field."""
        self.input_native.focus()


class CreateWordPage(HttpPostMixin, FormForeign):
    """Add word to foreign dictionary."""

    title = TITLE_FOREIGN_CREATE
    url = urljoin(HOST_API, FOREIGN_PATH)
    btn_submit_name = 'Добавить'

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            FOREIGN_WORD: self.input_foreign.value,
            RUSSIAN_WORD: self.input_native.value,
        }
        return submit_entry


class UpdateWordPage(HttpPutMixin, FormForeign):
    """Update the foreign word the box."""

    title = TITLE_FOREIGN_UPDATE
    url = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    btn_submit_name = 'Изменить'

    def handle_success(self, widget: toga.Widget) -> None:
        """Go to foreign list page, if success."""
        goto_foreign_list(widget)

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'id': str(self.entry.id),
            FOREIGN_WORD: self.input_foreign.value,
            RUSSIAN_WORD: self.input_native.value,
        }
        return submit_entry


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
            on_press=goto_foreign_main,
        )

        # Page widgets DOM.
        self.add(
            self.label_title,
            self.btn_goto_foreign_main,
            self.btns_manage,
            self.table,
            self.btns_paginate,
        )

    def create_handler(self, widget: toga.Widget) -> None:
        """Go to create the word form, button handler."""
        goto_foreign_create(widget)

    def update_handler(self, widget: toga.Widget) -> None:
        """Go to create the word form, button handler."""
        entry = self.table.selection
        update_box = self.root.app.box_foreign_update
        update_box.entry = entry
        self.set_window_content(widget, update_box)

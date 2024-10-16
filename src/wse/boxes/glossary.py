"""Glossary page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga

from wse.boxes.base import (
    BaseBox,
)
from wse.constants import (
    GLOSSARY_BOX,
    GLOSSARY_EXERCISE_BOX,
    GLOSSARY_EXERCISE_PATH,
    GLOSSARY_PARAMS_BOX,
    GLOSSARY_PARAMS_PATH,
    GLOSSARY_PROGRESS_PATH,
    HOST_API,
    MAIN_BOX,
)
from wse.contrib.http_requests import request_get, request_post
from wse.widgets.base import BtnApp
from wse.widgets.exercise import (
    ExerciseBox,
    ExerciseParamsSelectionsBox,
)


class GlossaryBox(BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = BtnApp(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        btn_goto_params_box = BtnApp(
            'Упражнение',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_params_box,
        )


class GlossaryParamsBox(BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_glossary_box = BtnApp(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_BOX),
        )
        btn_goto_glossary_exercise_box = BtnApp(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )
        btn_save_params = BtnApp(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )
        self.params_box = ExerciseParamsSelectionsBox()

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            self.params_box,
            btn_save_params,
            btn_goto_glossary_exercise_box,
        )

    async def goto_exercise_box_handler(self, widget: toga.Button) -> None:
        """Go to glossary exercise, button handler."""
        exercise_box = self.get_box(widget, GLOSSARY_EXERCISE_BOX)
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
        url = urljoin(HOST_API, GLOSSARY_PARAMS_PATH)
        response = request_get(url=url)
        if response.status_code == HTTPStatus.OK:
            self.params_box.fill_params(response.json())

    def save_params_handler(self, _: toga.Button) -> None:
        """Save Glossary Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(HOST_API, GLOSSARY_PARAMS_PATH)
        request_post(url, self.params_box.lookup_conditions)


class GlossaryExerciseBox(ExerciseBox):
    """English exercise box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.url_exercise = urljoin(HOST_API, GLOSSARY_EXERCISE_PATH)
        self.url_progress = urljoin(HOST_API, GLOSSARY_PROGRESS_PATH)

        # Buttons.
        btn_goto_glossary_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_BOX),
        )
        btn_goto_params_box = BtnApp(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            btn_goto_params_box,
            self.exercise_box,
        )

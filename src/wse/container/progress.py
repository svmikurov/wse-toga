"""Container for choice exercise progress parameters.

Choice parameters for exercises:
    * Glossary term study exercise
    * Foreign word study exercise
"""

import toga
from toga.style import Pack

from wse.widgets.box_page import BoxApp


class ProgressWidgets(BoxApp):
    """Progress widgets for exercise params boxes."""

    STUDY_STAGES = {
        'S': 'study_stage',
        'R': 'repeat_stage',
        'E': 'examination_stage',
        'K': 'know_stage',
    }

    def __init__(self) -> None:
        """Construct the progress widgets."""
        super().__init__()
        self.study_stage = True
        self.repeat_stage = False
        self.examination_stage = False
        self.know_stage = False

        # Style.
        switch_style = Pack(padding=(7, 0, 7, 20))
        label_style = Pack(padding=(7, 0, 7, 20))

        # Box widgets.
        # switches (checkboxes).
        self.sw_study_stage = toga.Switch(
            'Изучаю',
            value=self.study_stage,
            style=switch_style,
            on_change=self.study_stage_handler,
        )
        self.sw_repeat_stage = toga.Switch(
            'Повторяю',
            value=self.repeat_stage,
            style=switch_style,
            on_change=self.repeat_stage_handler,
        )
        self.sw_examination_stage = toga.Switch(
            'Проверяю',
            value=self.examination_stage,
            style=switch_style,
            on_change=self.examination_stage_handler,
        )
        self.sw_know_stage = toga.Switch(
            'Знаю',
            value=self.know_stage,
            style=switch_style,
            on_change=self.know_stage_handler,
        )
        # label
        self.progress_label = toga.Label('Этап изучения:', style=label_style)
        # boxes
        self.box_stages = toga.Box()

        # Widget DOM.
        self.box_stages.add(
            self.sw_study_stage,
            self.sw_repeat_stage,
            self.sw_examination_stage,
            self.sw_know_stage,
        )

    def study_stage_handler(self, widget: toga.Switch) -> None:
        """Choice study stage, switch handler."""
        self.study_stage = bool(widget.value)

    def repeat_stage_handler(self, widget: toga.Switch) -> None:
        """Choice repeat stage, switch handler."""
        self.repeat_stage = bool(widget.value)

    def examination_stage_handler(self, widget: toga.Switch) -> None:
        """Choice examination stage, switch handler."""
        self.examination_stage = bool(widget.value)

    def know_stage_handler(self, widget: toga.Switch) -> None:
        """Choice know stage, switch handler."""
        self.know_stage = bool(widget.value)

    @property
    def progress(self) -> list[str]:
        """Term study progress choices (`list[str]`, reade-only)."""
        progress_choices = []
        for alias, stage in self.STUDY_STAGES.items():
            if getattr(self, stage):
                progress_choices.append(alias)
        return progress_choices

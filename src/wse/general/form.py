"""Form class."""

from wse.general.box_page import BoxApp
from wse.general.data import ManagingWidgetDataFromResponse


class BaseForm(
    BoxApp,
    ManagingWidgetDataFromResponse,
):
    """Base form widget class."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)

    def on_open(self) -> None:
        """Invoke the focus to input field on open form."""
        self.focus_to_input_field()

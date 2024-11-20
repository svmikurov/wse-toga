"""The source of info text panel at main page."""
from gi.overrides.GLib import Source


class TextPanelMain(Source):
    """The info text panel source."""

    def __init__(self) -> None:
        """Construct the source."""
        super().__init__()
        self._value = None

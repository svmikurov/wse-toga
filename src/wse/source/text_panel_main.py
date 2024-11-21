"""The source of info text panel at main page."""

from toga.sources import Source

from wse.constants import HOST_API
from wse.source.user import UserSource


class MainPanelSource(Source):
    """The info text panel source."""

    welcome = f'Ready for connect to {HOST_API}'
    """Welcome text on the information display (`str`).
    """
    text_user_info = 'Добро пожаловать, %s!'
    """User info text (`str`).
    """

    def __init__(self, source_user: UserSource) -> None:
        """Construct the source."""
        super().__init__()
        self._value = ''
        self.source_user = source_user

    def update_text(self) -> None:
        """Update info text by source_user auth status."""
        if self.source_user.is_auth:
            self._value = self.text_user_info % self.source_user.username
        else:
            self._value = self.welcome

    @property
    def value(self) -> str | None:
        """Return text to display (`str`, reade-only)."""
        self.update_text()
        return self._value

"""The source of info text panel at main page."""

from toga.sources import Source

from wse.constants import HOST_API
from wse.source.user import UserSource


class MainInfoPanelSource(Source):
    """The source for info text panel at main box-container."""

    welcome = f'Ready for connect to {HOST_API}'
    """Welcome text on the information display (`str`).
    """
    text_user_info = 'Добро пожаловать, %s!'
    """User info text (`str`).
    """

    def __init__(self, user: UserSource) -> None:
        """Construct the source."""
        super().__init__()
        self._value = ''
        self.user = user

    def update_text(self) -> str:
        """Update info text by user auth status."""
        if self.user.is_auth:
            self._value = self.text_user_info % self.user.username
        else:
            self._value = self.welcome
        return self._value

    @property
    def value(self) -> str | None:
        """Return text to display (`str`, reade-only)."""
        self.update_text()
        return self._value

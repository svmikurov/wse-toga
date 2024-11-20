"""User data source."""

from toga.sources import Source


class UserSource(Source):
    """User data source."""

    def __init__(self) -> None:
        """Construct the source."""
        super().__init__()
        self._username: str | None = None
        self._is_auth: bool = False

    @property
    def username(self) -> str:
        """The username (`str`)."""
        return self._username

    @username.setter
    def username(self, value) -> None:
        self._username = value

    @property
    def is_auth(self) -> bool:
        """The user auth status (`bool`)."""
        return self._is_auth

    @is_auth.setter
    def is_auth(self, value) -> None:
        self._is_auth = value

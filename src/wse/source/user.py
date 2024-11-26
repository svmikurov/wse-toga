"""User data source."""

import json
import os
from http import HTTPStatus
from pathlib import Path

from toga.sources import Source

from wse.contrib.http_requests import request_user_data, app_auth

PATH_USERDATA_FILE = os.path.join(
    Path(__file__).parent.parent,
    'resources/userdata.json',
)


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

    @property
    def is_auth(self) -> bool:
        """The source_user auth status (`bool`)."""
        return self._is_auth

    def set_source_user(self, userdata: dict) -> None:
        """Set user source."""
        self._username = userdata.get('username')
        self._is_auth = True if self._username else False

    @staticmethod
    def save_userdata(userdata: dict) -> None:
        """Save user data."""
        with open(PATH_USERDATA_FILE, 'w', encoding='utf-8') as fp:
            json.dump(userdata, fp, ensure_ascii=False, indent=4)

    def delete_userdata(self) -> None:
        """Delete user data."""
        self._username = None
        self._is_auth = False
        self.delete_userdata_fail()

    @staticmethod
    def delete_userdata_fail() -> None:
        """Delete the userdata fail."""
        try:
            os.unlink(PATH_USERDATA_FILE)
        except FileNotFoundError:
            pass

    def load_userdata(self) -> None:
        """Load user data on start app."""
        try:
            with open(PATH_USERDATA_FILE, 'r') as file:
                userdata = json.load(file)
        except FileNotFoundError:
            print('INFO: User data was not saved')
            pass
        else:
            self.set_source_user(userdata)

    def on_start(self) -> None:
        """Set user data on start app."""
        response = request_user_data()

        if response.status_code == HTTPStatus.OK:
            userdata = response.json()
            self.set_source_user(userdata)
            self.save_userdata(userdata)
        elif response.status_code == HTTPStatus.UNAUTHORIZED:
            self.delete_userdata()
            del app_auth.token

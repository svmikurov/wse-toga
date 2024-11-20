"""Utils for testing."""

import asyncio
import json
import os
import pathlib

from wse.app import WSE


def run_until_complete(wse: WSE) -> object:
    """Run the event loop until a Future is done."""
    time_to_sleep = 0.1
    return wse.loop.run_until_complete(asyncio.sleep(time_to_sleep))


class FixtureReader:
    """Reader of fixtures.

    :param str fixture: The fixture file name.
    """

    module_dir = pathlib.Path(__file__).parent
    """Current module dir path (`str`).
    """

    def __init__(self, fixture_file_name: str) -> None:
        """Construct the reader."""
        self.fixture = fixture_file_name

    @property
    def fixture_path(self) -> str:
        """Return the path to fixture (`str`, reade-only)."""
        return os.path.join(self.module_dir, f'fixtures/{self.fixture}')

    @staticmethod
    def url() -> str:
        """Return the url."""
        return ''

    def json(self) -> dict:
        """Reade the fixture.

        :return: the fixture data.
        """  # noqa: D401
        with open(self.fixture_path, 'r') as file:
            fixture = json.load(file)
        return fixture

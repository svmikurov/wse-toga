"""Event time control."""

import asyncio

from wse.constants import DEFAULT_TIMEOUT


class Timer:
    """Event time control."""

    def __init__(self) -> None:
        """Construct the time control."""
        self.timer = None
        self.pause = False
        self.timeout = DEFAULT_TIMEOUT

    async def start(self) -> None:
        """Start event timer."""
        self.timer = asyncio.create_task(asyncio.sleep(self.timeout))
        await self.timer

    def is_timer(self) -> bool:
        """Is the timer started."""
        return True if self.timer else False

    def cancel(self) -> None:
        """Cancel event timer."""
        if self.is_timer():
            self.timer.cancel()

    def on_pause(self) -> None:
        """Pause the event."""
        self.pause = True

    def is_pause(self) -> bool:
        """Is the event paused."""
        return self.pause

    def unpause(self) -> None:
        """Unpause the event."""
        self.pause = False

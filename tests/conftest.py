import asyncio
import sys

import pytest

import toga


@pytest.fixture(scope="module")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


class TestApp(toga.App):
    def startup(self):
        # Ensure that Toga's task factory is tracking all tasks
        toga_task_factory = self.loop.get_task_factory()

        def task_factory(loop, coro, context=None):
            if sys.version_info < (3, 11):
                task = toga_task_factory(loop, coro)
            else:
                task = toga_task_factory(loop, coro, context=context)
            assert task in self._running_tasks, f"missing task reference for {task}"
            return task

        self.loop.set_task_factory(task_factory)
        super().startup()


@pytest.fixture
def app(event_loop):
    # The app icon is cached; purge the app icon cache if it exists
    try:
        del toga.Icon.__APP_ICON
    except AttributeError:
        pass

    return TestApp(formal_name="Test App", app_id="org.beeware.toga.test-app")


@pytest.fixture
def window(app):
    return toga.Window()

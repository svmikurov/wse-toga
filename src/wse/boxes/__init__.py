"""App boxes to assign to window content."""

from wse.boxes.foreign import (
    ForeignCreatePage,
    ForeignExercisePage,
    ForeignListPage,
    ForeignMainPage,
    ForeignParamsPage,
    ForeignUpdatePage,
)
from wse.boxes.glossary import (
    GlossaryBox,
    GlossaryExerciseBox,
    GlossaryParamsBox,
)
from wse.boxes.main import (
    MainBox,
)
from wse.boxes.user import (
    LoginBox,
    UserBox,
    UserCreateBox,
)

__all__ = (
    'ForeignCreatePage',
    'ForeignExercisePage',
    'ForeignListPage',
    'ForeignMainPage',
    'ForeignParamsPage',
    'ForeignUpdatePage',
    'GlossaryBox',
    'GlossaryExerciseBox',
    'GlossaryParamsBox',
    'LoginBox',
    'MainBox',
    'UserBox',
    'UserCreateBox',
)

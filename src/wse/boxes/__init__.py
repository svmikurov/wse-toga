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
    CreateTermPage,
    GlossaryExerciseBox,
    GlossaryMainPage,
    GlossaryParamsBox,
    ListTermPage,
    UpdateTermPage,
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
    'CreateTermPage',
    'GlossaryExerciseBox',
    'ListTermPage',
    'GlossaryMainPage',
    'GlossaryParamsBox',
    'UpdateTermPage',
    'LoginBox',
    'MainBox',
    'UserBox',
    'UserCreateBox',
)

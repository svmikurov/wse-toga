"""App boxes to assign to window content."""

from wse.page.foreign import (
    CreateForeignPage,
    ForeignExercisePage,
    ListForeignPage,
    MainForeignPage,
    ParamsForeignPage,
    UpdateForeignPage,
)
from wse.page.glossary import (
    CreateTermPage,
    ExerciseGlossaryBox,
    ListTermPage,
    MainGlossaryPage,
    ParamsGlossaryBox,
    UpdateTermPage,
)
from wse.page.main import (
    MainBox,
)
from wse.page.user import (
    AuthBox,
    UserBox,
    UserUpdateBox,
)

__all__ = (
    'AuthBox',
    'CreateForeignPage',
    'CreateTermPage',
    'ExerciseGlossaryBox',
    'ForeignExercisePage',
    'ListForeignPage',
    'ListTermPage',
    'MainBox',
    'MainForeignPage',
    'MainGlossaryPage',
    'ParamsForeignPage',
    'ParamsGlossaryBox',
    'UpdateForeignPage',
    'UpdateTermPage',
    'UserBox',
    'UserUpdateBox',
)

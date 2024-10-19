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
    LoginBox,
    UserBox,
    UserCreateBox,
)

__all__ = (
    'CreateForeignPage',
    'ForeignExercisePage',
    'ListForeignPage',
    'MainForeignPage',
    'ParamsForeignPage',
    'UpdateForeignPage',
    'CreateTermPage',
    'ExerciseGlossaryBox',
    'ListTermPage',
    'MainGlossaryPage',
    'ParamsGlossaryBox',
    'UpdateTermPage',
    'LoginBox',
    'MainBox',
    'UserBox',
    'UserCreateBox',
)

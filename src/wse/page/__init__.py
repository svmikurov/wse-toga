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
    CreateUserBox,
    LoginBox,
    MainUserBox,
    UpdateUserBox,
)

__all__ = (
    'CreateForeignPage',
    'CreateTermPage',
    'CreateUserBox',
    'ExerciseGlossaryBox',
    'ForeignExercisePage',
    'ListForeignPage',
    'ListTermPage',
    'LoginBox',
    'MainBox',
    'MainForeignPage',
    'MainGlossaryPage',
    'MainUserBox',
    'ParamsForeignPage',
    'ParamsGlossaryBox',
    'UpdateForeignPage',
    'UpdateTermPage',
    'UpdateUserBox',
    'UpdateUserBox',
)

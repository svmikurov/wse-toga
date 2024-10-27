"""App boxes to assign to window content."""

from wse.page.foreign import (
    CreateWordPage,
    ExerciseForeignPage,
    ListForeignPage,
    MainForeignPage,
    ParamForeignPage,
    UpdateWordPage,
)
from wse.page.glossary import (
    CreateTermPage,
    ExerciseGlossaryBox,
    ListTermPage,
    MainGlossaryPage,
    ParamGlossaryBox,
    UpdateTermPage,
)
from wse.page.main import (
    MainBox,
)
from wse.page.user import (
    LoginBox,
)

__all__ = (
    'CreateWordPage',
    'CreateTermPage',
    'ExerciseGlossaryBox',
    'ExerciseForeignPage',
    'ListForeignPage',
    'ListTermPage',
    'LoginBox',
    'MainBox',
    'MainForeignPage',
    'MainGlossaryPage',
    'ParamForeignPage',
    'ParamGlossaryBox',
    'UpdateWordPage',
    'UpdateTermPage',
)

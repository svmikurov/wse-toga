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
    ExerciseGlossaryPage,
    ListTermPage,
    MainGlossaryPage,
    ParamGlossaryPage,
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
    'ExerciseGlossaryPage',
    'ExerciseForeignPage',
    'ListForeignPage',
    'ListTermPage',
    'LoginBox',
    'MainBox',
    'MainForeignPage',
    'MainGlossaryPage',
    'ParamForeignPage',
    'ParamGlossaryPage',
    'UpdateWordPage',
    'UpdateTermPage',
)

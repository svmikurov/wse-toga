"""App boxes to assign to window content."""

from wse.pages.foreign import (
    CreateWordPage,
    ExerciseForeignPage,
    ListForeignPage,
    MainForeignPage,
    ParamForeignPage,
    UpdateWordPage,
)
from wse.pages.glossary import (
    CreateTermPage,
    ExerciseGlossaryPage,
    ListTermPage,
    MainGlossaryPage,
    ParamGlossaryPage,
    UpdateTermPage,
)
from wse.pages.login import LoginBox
from wse.pages.main import (
    MainBox,
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

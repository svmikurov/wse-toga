"""App boxes to assign to window content."""

from wse.boxes.foreign import (
    EnglishBox,
    EnglishExerciseBox,
    EnglishParamsBox,
)
from wse.boxes.glossary import (
    GlossaryBox,
    GlossaryExerciseBox,
    GlossaryParamsBox,
)
from wse.boxes.main import MainBox
from wse.boxes.user import (
    LoginBox,
    UserBox,
)
from wse.boxes.word import WordBox

__all__ = (
    'EnglishBox',
    'EnglishExerciseBox',
    'EnglishParamsBox',
    'GlossaryBox',
    'GlossaryExerciseBox',
    'GlossaryParamsBox',
    'LoginBox',
    'MainBox',
    'UserBox',
    'WordBox',
)

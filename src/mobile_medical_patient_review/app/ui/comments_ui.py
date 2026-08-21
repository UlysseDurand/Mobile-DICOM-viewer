from dataclasses import dataclass

from trame.widgets.html import H1
from trame.widgets.vuetify3 import (
    VCard,
    VCardTitle,
    VTextarea,
)

from .abstract.abstract_ui import AbstractUI


@dataclass
class CommentsState:
    text: str = ""


class CommentsUI(VCard, AbstractUI[CommentsState]):
    def __init__(self, **kwargs: dict) -> None:
        VCard.__init__(self, **kwargs)
        AbstractUI.__init__(self, self.state, CommentsState)

    def _build_ui(self) -> None:
        with self:
            VCardTitle("Comments")
            VTextarea(label="Comment This scan")

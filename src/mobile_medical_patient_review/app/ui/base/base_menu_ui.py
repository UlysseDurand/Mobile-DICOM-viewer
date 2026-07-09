from abc import abstractmethod
from typing import TypeVar

from trame.widgets.vuetify3 import VCard

from ..abstract.abstract_ui import AbstractUI

T = TypeVar("T")

class BaseMenuUI(VCard, AbstractUI[T]):
    def __init__(self, **kwargs: dict):
        VCard.__init__(self, **kwargs)
        AbstractUI.__init__(self, self.state, self.state_type)

    def _build_ui(self) -> None:
        super()._build_ui()
        with self:
            pass

    @property
    @abstractmethod
    def state_type(self) -> T:
        pass

    @property
    @abstractmethod
    def label(self) -> str:
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        pass

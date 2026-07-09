from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from .abstract_ui import AbstractUI

E = TypeVar('E')
@dataclass
class AbstractSelectState(Generic[E]):
    selected: E = field(default=None)

class AbstractSelectUI(AbstractUI[AbstractSelectState[E]], Generic[E]):
    def __init__(self, state_class: type[AbstractSelectState[E]], *args: Any, **kwargs: Any):
        AbstractUI.__init__(self, self.state, state_class, *args, **kwargs)

    def is_selected(self, option: E) -> tuple[str,]:
        return self._state_equal(self.name.selected, option)

    def select(self, option: E) -> None:
        self.data.selected = option
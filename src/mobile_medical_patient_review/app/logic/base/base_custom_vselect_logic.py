from typing import Generic

from trame_slicer.app.logic import BaseLogic

from ...ui.abstract.abstract_select_ui import AbstractSelectState, E


class BaseCustomVSelectLogic(Generic[E], BaseLogic[AbstractSelectState[E]]):
    def is_selected(self, option: E) -> bool:
        return self.data.selected == option
from dataclasses import dataclass

from ..abstract.abstract_select_ui import AbstractSelectState
from ..base.base_menu_selector_ui import BaseMenuSelectorUI
from ..base.base_menu_ui import BaseMenuUI
from .annotator_menu_ui import AnnotatorMenuUI
from .volume_menu_ui import VolumeMenuUI

menus = [
    VolumeMenuUI, 
    AnnotatorMenuUI
]

@dataclass
class MainMenuSelectorState(AbstractSelectState[type[BaseMenuUI]]):
    selected: str = "AnnotatorMenuUI"

class MainMenuSelectorUI(BaseMenuSelectorUI):
    def __init__(self) -> None:
        super().__init__(MainMenuSelectorState, menus)

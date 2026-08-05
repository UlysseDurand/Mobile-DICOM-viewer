from dataclasses import dataclass
from enum import Enum, auto

from .abstract.abstract_select_ui import AbstractSelectState
from .base.base_custom_vselect_ui import BaseCustomVSelectUI


class SingleTouchFunctionsEnum(Enum):
    SLICE = auto()
    ZOOM = auto()
    PAN = auto()
    CONTRAST = auto()
    NONE = auto()

single_touch_functions = {
    SingleTouchFunctionsEnum.SLICE: {"name": "Slice", "icon": "mdi-arrow-up-down-bold"},
    SingleTouchFunctionsEnum.ZOOM: {"name": "Zoom", "icon": "mdi-magnify-plus"},
    SingleTouchFunctionsEnum.PAN: {"name": "Pan", "icon": "mdi-arrow-all"},
    SingleTouchFunctionsEnum.CONTRAST: {"name": "Window level", "icon": "mdi-contrast-box"},
    SingleTouchFunctionsEnum.NONE: {"name": "Do nothing", "icon": "mdi-cursor-default"},
}

@dataclass
class SingleTouchFunctionsState(AbstractSelectState[SingleTouchFunctionsEnum]):
    selected: SingleTouchFunctionsEnum = SingleTouchFunctionsEnum.SLICE

class SingleTouchFunctionsUI(BaseCustomVSelectUI[SingleTouchFunctionsEnum]):
    def __init__(self) -> None:
        super().__init__(SingleTouchFunctionsState, "Single-touch function", single_touch_functions)
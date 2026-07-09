from dataclasses import dataclass, field

from trame.widgets.html import Span
from trame.widgets.vuetify3 import VBtn
from undo_stack import Signal

from ..base.base_menu_ui import BaseMenuUI


@dataclass
class VolumeMenuState:
    available_volumes: list[str] = field(default_factory=list)

class VolumeMenuUI(BaseMenuUI[VolumeMenuState]):
    icon = "mdi-cube"
    label = "Volume selection"
    state_type = VolumeMenuState

    load_volume = Signal(str)

    def _build_ui(self) -> None:
        super()._build_ui()
        with self:
            for volume in self.data.available_volumes:
                with VBtn(
                    click = lambda v=volume: self.load_volume(v),
                    classes="ma-2"
                ):
                    Span(f"Load {volume}")
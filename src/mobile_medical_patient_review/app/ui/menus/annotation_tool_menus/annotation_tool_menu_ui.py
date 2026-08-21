from dataclasses import dataclass, field

from trame.widgets.vuetify3 import VBtn, VBtnGroup, VCard, VIcon, VTooltip
from undo_stack import Signal

from ...abstract.abstract_select_ui import AbstractSelectState
from ...base.base_menu_selector_ui import BaseMenuSelectorUI
from ...base.base_menu_ui import BaseMenuUI
from .angle_tool_menu_ui import AngleToolMenuUI
from .closed_curve_tool_menu_ui import ClosedCurveToolMenuUI
from .fiducial_tool_menu_ui import FiducialToolMenuUI
from .open_curve_tool_menu_ui import OpenCurveToolMenuUI
from .plane_tool_menu_ui import PlaneToolMenuUI
from .roi_tool_menu_ui import RoiToolMenuUI
from .ruler_tool_menu_ui import RulerToolMenuUI

menus = [
    FiducialToolMenuUI,
    RulerToolMenuUI,
    AngleToolMenuUI,
    OpenCurveToolMenuUI,
    ClosedCurveToolMenuUI,
    PlaneToolMenuUI,
    RoiToolMenuUI,
]

@dataclass
class AnnotationToolMenuState(AbstractSelectState[type[BaseMenuUI]]):
    selected: str | None = None

class AnnotationToolMenuUI(BaseMenuSelectorUI):
    clear_clicked = Signal()

    def __init__(self) -> None:
        super().__init__(AnnotationToolMenuState, menus)

    def deselect(self) -> None:
        self.data.selected = None

    def _is_no_tool_selected(self) -> tuple[str,]:
        return self._state_equal(self.name.selected, None)

    def _build_ui(self, items: list[type[BaseMenuUI]]) -> None:
        with self:
            with VBtnGroup():
                with VBtn(
                    icon=True,
                    click=self.deselect,
                    active=self._is_no_tool_selected(),
                ):
                    VIcon("mdi-cursor-default")
                    VTooltip("No Markup Tool", activator="parent", location="top")
                for menu in items:
                    with VBtn(
                        icon=True,
                        click=lambda m=menu: self.select(m),
                        active=self.is_selected(menu),
                    ):
                        VIcon(menu.icon)
                        VTooltip(menu.label, activator="parent", location="top")
                with VBtn(
                    icon=True,
                    click=self.clear_clicked.emit,
                    color="error",
                    variant="text",
                ):
                    VIcon("mdi-trash-can-outline")
                    VTooltip("Clear Markups", activator="parent", location="top")
            with VCard():
                for menu in items:
                    ui_instance = menu(v_if=self.is_selected(menu))
                    self._menu_instances[menu] = ui_instance

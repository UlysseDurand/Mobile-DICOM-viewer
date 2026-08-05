from ..base.base_menu_ui import BaseMenuUI
from .annotation_tool_menus.annotation_tool_menu_ui import AnnotationToolMenuUI


class AnnotatorMenuUI(BaseMenuUI[None]):
    icon = "mdi-brush"
    label = "Annotation"
    state_type = None

    def _build_ui(self) -> None:
        super()._build_ui()
        with self:
            self.tool_menu = AnnotationToolMenuUI()

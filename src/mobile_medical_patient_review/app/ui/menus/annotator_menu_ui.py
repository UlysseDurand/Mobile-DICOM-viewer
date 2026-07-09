from ..base.base_menu_ui import BaseMenuUI


class AnnotatorMenuUI(BaseMenuUI[None]):
    icon = "mdi-brush"
    label = "Annotation"
    state_type = None
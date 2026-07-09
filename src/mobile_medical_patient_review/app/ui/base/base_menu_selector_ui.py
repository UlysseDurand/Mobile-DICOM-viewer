from trame.widgets.vuetify3 import VBtn, VBtnGroup, VCard, VIcon, VTooltip

from ..abstract.abstract_select_ui import AbstractSelectState, AbstractSelectUI
from .base_menu_ui import BaseMenuUI

E = str
class BaseMenuSelectorUI(VCard, AbstractSelectUI[E]):
    def __init__(
        self, 
        state_class:type[AbstractSelectState[E]], 
        items: list[BaseMenuUI], 
    ):
        self._menu_instances: dict[type[BaseMenuUI], BaseMenuUI] = {}

        VCard.__init__(self)
        AbstractSelectUI.__init__(self, state_class, items)
    
    def _build_ui(self, items: list[E]) -> None:
        with self:
            with VBtnGroup():
                for menu in items:
                    with VBtn(
                        icon=True,
                        click=lambda m=menu: self.select(m),
                        active=self.is_selected(menu)
                    ):
                        VIcon(menu.icon)
                        VTooltip(menu.label, activator="parent", location="top")
            with VCard():
                for menu in items:
                    ui_instance = menu(v_if=self.is_selected(menu))
                    self._menu_instances[menu] = ui_instance

    def is_selected(self, option: type[BaseMenuUI]) -> tuple[str,]:
        return AbstractSelectUI.is_selected(self, option.__name__)
    
    def select(self, option: type[BaseMenuUI]) -> None:
        AbstractSelectUI.select(self, option.__name__)

    def get_menu_ui(self, menu_key: type[BaseMenuUI]) -> BaseMenuUI:
            return self._menu_instances[menu_key]

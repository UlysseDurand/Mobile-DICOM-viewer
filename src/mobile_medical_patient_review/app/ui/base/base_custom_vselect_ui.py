from typing import Generic

from trame.widgets.html import Div
from trame.widgets.vuetify3 import Template, VCard, VCardText, VMenu, VRow

from ..abstract.abstract_select_ui import AbstractSelectState, AbstractSelectUI, E
from ..control_button_ui import ControlButton


class BaseCustomVSelectUI(VMenu, AbstractSelectUI[E], Generic[E]):
    def __init__(
        self, 
        state_class:type[AbstractSelectState[E]], 
        name: str, 
        items: dict[E, dict], 
    ):
        VMenu.__init__(self, close_on_content_click=True, location="bottom")
        AbstractSelectUI.__init__(self, state_class, name, items)

    def _build_ui(self, name: str, items: dict[E, dict]) -> None:
        with self:
            with Template(v_slot_activator="{ props }"):
                for item_key, item_options in items.items():
                    ControlButton(
                        v_if=self.is_selected(item_key),
                        name=name, icon=item_options["icon"], v_bind="props"
                    )

            with VCard(), VCardText(), VRow(), Div(classes="d-flex flex-column"):
                for item_key, item_options  in items.items():
                    ControlButton(
                        name=item_options["name"],
                        icon=item_options["icon"], 
                        click = lambda v=item_key: self.select(v)
                    )
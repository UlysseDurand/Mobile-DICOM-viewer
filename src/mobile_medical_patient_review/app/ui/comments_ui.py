from trame.widgets.vuetify3 import (
    Template,
    VCard,
    VCardText,
    VCardTitle,
    VIcon,
    VList,
    VListItem,
    VTextarea,
)
from trame_server.utils.typed_state import TypedState
from undo_stack import Signal

from .menus.annotation_tool_menus.annotation_tool_menu_ui import AnnotationToolMenuState


class CommentsUI(VCard):
    comment_changed = Signal(str, str)

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)
        self._typed_state = TypedState(self.state, AnnotationToolMenuState)
        self._build_ui()

    def _build_ui(self) -> None:
        with self:
            VCardTitle("Comments")
            VCardText(
                "No annotations yet. Use the Annotation menu to add one.",
                v_if=(f"{self._typed_state.name.annotations}.length === 0",),
            )
            with VList(v_if=(f"{self._typed_state.name.annotations}.length > 0",)):
                with VListItem(
                    v_for=f"(item, i) in {self._typed_state.name.annotations}",
                    key="i",
                    value="item",
                ):
                    with Template(v_slot_prepend=True):
                        VIcon(icon=("item.icon",))
                    with Template(v_slot_default=True):
                        VTextarea(
                            label=("item.type_label + ' - ' + item.name",),
                            v_model=("item.comment",),
                            change=self._comment_change_js(),
                            auto_grow=True,
                            rows=2,
                            density="compact",
                            hide_details=True,
                        )

    def _comment_change_js(self) -> str:
        return f"trigger('{self.server.trigger_name(self.comment_changed)}', [item.node_id, item.comment]);"

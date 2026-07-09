from __future__ import annotations

from typing import TYPE_CHECKING, Any

from trame_server.utils.typed_state import TypedState
from trame_slicer.app.logic import get_view_trame_id

from ..ui.slice_nb_ui import SliceNbState

if TYPE_CHECKING:
    from trame_server.core import Server
    from trame_slicer.views.abstract_view import AbstractViewChild
    from trame_slicer.views.slice_view import SliceView


def get_view_slider_typed_state(server: Server, view: AbstractViewChild) -> TypedState[SliceNbState]:
    """
    :return: Typed state associated with input view
    """
    return TypedState(server.state, SliceNbState, namespace=get_view_trame_id(server, view))


def connect_slice_nb_view_to_state(
    server: Server,
    view: SliceView,
    *_: Any,
) -> TypedState[SliceNbState]:
    slice_nb_state = get_view_slider_typed_state(server, view)

    def _on_slice_view_modified(view: SliceView) -> None:
        range_min, range_max = view.get_slice_range()
        resolution = view.get_slice_step()
        offset = view.get_slice_value()

        slice_index = round((offset - range_min) / resolution)
        max_slice = round((range_max - range_min) / resolution)
        with server.state:
            slice_nb_state.data.slice_nb = slice_index
            slice_nb_state.data.max_slice = max_slice
        server.state.flush()

    view.modified.connect(_on_slice_view_modified)
    _on_slice_view_modified(view)
    return slice_nb_state
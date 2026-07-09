from __future__ import annotations

from typing import TYPE_CHECKING

from trame_client.widgets.html import Div

from ..logic.slice_view_logic import connect_slice_nb_view_to_state
from .slice_nb_ui import SliceNbUI

if TYPE_CHECKING:
    from trame_server.core import Server
    from trame_slicer.views import AbstractViewChild


def create_slice_nb_view_ui(
    server: Server,
    _view_id: str,
    view: AbstractViewChild,
) -> None:

    slice_nb_state = connect_slice_nb_view_to_state(server, view)
    with Div(
        classes="ma-5",
        style="position: absolute;bottom: 0;right: 0;",
    ):
        SliceNbUI(slice_nb_state)
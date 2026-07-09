from dataclasses import dataclass

from trame.widgets.html import H1
from trame_server.utils.typed_state import TypedState

from .abstract.abstract_ui import AbstractUI


@dataclass
class SliceNbState:
    max_slice: int = 1
    slice_nb: int = 0

class SliceNbUI(H1, AbstractUI):
    def __init__(self, typed_state: TypedState[SliceNbState]):
        vmodel = f"{ '{{'+str(typed_state.name.slice_nb)+'}}' } / { '{{'+str(typed_state.name.max_slice)+'}}'}"
        H1.__init__(self, vmodel, style="color: white")
        AbstractUI.__init__(self, self.state, SliceNbState, typed_state=typed_state)
    
    def _build_ui(self) -> None:
        with self:
            pass
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from trame_server.state import State
from trame_server.utils.typed_state import TypedState

T = TypeVar("T")

class AbstractUI(Generic[T], ABC):
    def __init__(
        self, 
        state: State, 
        state_type: Optional[type[T]] = None,
        *args: Any,
        typed_state: Optional[TypedState[T]] = None,
        **kwargs: Any
    ):
        self._typed_state = typed_state if typed_state else TypedState(state, state_type) if state_type else None
        self._build_ui(*args, **kwargs)

    @abstractmethod
    def _build_ui(self, *args: Any, **kwargs: Any) -> None:
        pass
    
    @property
    def name(self) -> T:
        return self._typed_state.name if self._typed_state else None
    
    @property
    def data(self) -> T:
        return self._typed_state.data if self._typed_state else None
    
    def _state_equal(self, state_name: str, value: Any) -> tuple[str,]:
        if isinstance(value, str):
            return (f"{state_name} == '{self._typed_state.encode(value)}'",)
        return (f"{state_name} == {self._typed_state.encode(value)}",)
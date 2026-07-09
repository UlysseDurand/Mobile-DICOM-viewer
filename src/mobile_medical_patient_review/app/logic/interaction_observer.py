from abc import ABC, abstractmethod

from trame_slicer.views.slice_view import SliceView


class InteractionObserver(ABC):
    @abstractmethod
    def on_start_drag(self) -> None:
        pass

    @abstractmethod
    def on_drag(self, view: SliceView, dx: float, dy: float, delta_x: float, delta_y: float) -> None:
        pass

    @abstractmethod
    def on_end_drag(self) -> None:
        pass

    @abstractmethod
    def on_start_pinch(self, view: SliceView, scale: float) -> None:
        pass

    @abstractmethod
    def on_pinch(self, view: SliceView, scale: float) -> None:
        pass

    @abstractmethod
    def on_end_pinch(self, view: SliceView, scale: float) -> None:
        pass

    @abstractmethod
    def on_start_pan(self, view: SliceView, translation: tuple[float, float]) -> None:
        pass

    @abstractmethod
    def on_pan(self, view: SliceView, translation: tuple[float, float]) -> None:
        pass

    @abstractmethod
    def on_end_pan(self, view: SliceView, translation: tuple[float, float]) -> None:
        pass

    @abstractmethod
    def on_start_rotate(self, view: SliceView, rotation: tuple[float, float]) -> None:
        pass

    @abstractmethod
    def on_rotate(self, view: SliceView, rotation: tuple[float, float]) -> None:
        pass

    @abstractmethod
    def on_end_rotate(self, view: SliceView, rotation: tuple[float, float]) -> None:
        pass

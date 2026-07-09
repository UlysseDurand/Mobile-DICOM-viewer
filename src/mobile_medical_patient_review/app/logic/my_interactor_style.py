from __future__ import annotations

from typing import TYPE_CHECKING

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage

if TYPE_CHECKING:

    from trame_slicer.views import (
        SliceView,
    )

    from .interaction_observer import InteractionObserver


class MyInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, slice_view: SliceView):
        self._slice_view = slice_view

        self._interaction_observers = []

        self._first_drag = (0, 0)
        self._last_drag = (0, 0)
        self._last_scale = 1
        self._delta_scale = 1
        self._last_pan = (0, 0)
        self._delta_pan = (0, 0)
        self._last_rot = (0, 0)
        self._delta_rot = (0, 0)

        self.AddObserver("MouseMoveEvent", self.on_drag)
        self.AddObserver("LeftButtonPressEvent", self.on_button_press)
        self.AddObserver("LeftButtonReleaseEvent", self.on_button_release)
        self.AddObserver("StartPinchEvent", self.on_start_pinch)
        self.AddObserver("PinchEvent", self.on_pinch)
        self.AddObserver("EndPinchEvent", self.on_end_pinch)
        self.AddObserver("StartPanEvent", self.on_start_pan)
        self.AddObserver("PanEvent", self.on_pan)
        self.AddObserver("EndPanEvent", self.on_end_pan)
        self.AddObserver("StartRotationEvent", self.on_start_rotation)
        self.AddObserver("RotationEvent", self.on_rotation)
        self.AddObserver("EndRotationEvent", self.on_end_rotation)

    def add_interaction_observer(self, interaction_observer: InteractionObserver) -> None:
        self._interaction_observers.append(interaction_observer)
    
    def on_button_press(self, obj, event) -> None:
        self._is_dragging = True
        self._first_drag = self.GetInteractor().GetEventPosition()
        self._last_drag = self._first_drag
        for observer in self._interaction_observers:
            observer.on_start_drag(self._slice_view)

    def on_button_release(self, obj, event) -> None:
        self._is_dragging = False
        for observer in self._interaction_observers:
            observer.on_end_drag(self._slice_view)

    def on_drag(self, obj, event) -> None:
        x, y = self.GetInteractor().GetEventPosition()
        if (self._is_dragging):
            delta_x = x - self._first_drag[0]
            delta_y = y - self._first_drag[1]
            dx = x - self._last_drag[0]
            dy = y - self._last_drag[1]
            self._last_drag = (x, y)

            for observer in self._interaction_observers:
                observer.on_drag(self._slice_view, dx, dy, delta_x, delta_y)
    
    def on_start_pinch(self, obj, event) -> None:
        scale = self.GetInteractor().GetScale()
        self._last_scale = scale
        self._delta_scale = 1

    def on_pinch(self, obj, event) -> None:
        scale = self.GetInteractor().GetScale()
        
        dscale = scale / self._last_scale
        self._last_scale = scale

        self._delta_scale = self._delta_scale * dscale

        for observer in self._interaction_observers:
            observer.on_pinch(self._slice_view, dscale, self._delta_scale)

    def on_end_pinch(self, obj, event) -> None:
        pass

    def on_start_pan(self, obj, event) -> None:
        pan = self.GetInteractor().GetTranslation()
        self._last_pan = pan
        self._delta_pan = (0, 0)

    def on_pan(self, obj, event) -> None:
        pan = self.GetInteractor().GetTranslation()

        dpan = (pan[0] - self._last_pan[0], pan[1] - self._last_pan[1])
        self._last_pan = pan
        self.delta_pan = (self._delta_pan[0] + dpan[0], self._delta_pan[1] + dpan[1])

        for observer in self._interaction_observers:
            observer.on_pan(self._slice_view, dpan, self._delta_pan)

    def on_end_pan(self, obj, event) -> None:
        pass

    def on_start_rotation(self, obj, event) -> None:
        rot = self.GetInteractor().GetRotation()
        self._last_rot = rot
        self._delta_rot = rot

    def on_rotation(self, obj, event) -> None:
        rot = self.GetInteractor().GetRotation()

        drot = (rot[0] - self._last_rot[0], rot[1] - self._last_rot[1])
        self._last_rot = rot
        self.delta_rot = (self._delta_rot[0] + drot[0], self._delta_rot[1] + drot[1])

        for observer in self._interaction_observers:
            observer.on_rot(self._slice_view, drot, self._delta_rot)

    def on_end_rotation(self, obj, event) -> None:
        pass

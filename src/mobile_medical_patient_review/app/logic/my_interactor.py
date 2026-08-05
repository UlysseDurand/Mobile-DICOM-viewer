from __future__ import annotations

from math import exp, log
from typing import TYPE_CHECKING, Any

from trame_slicer.core import SlicerApp, VolumeWindowLevel

from ..ui.single_touch_functions_ui import (
    SingleTouchFunctionsEnum,
    SingleTouchFunctionsState,
)
from .base.base_custom_vselect_logic import BaseCustomVSelectLogic

if TYPE_CHECKING:
    from trame_server import Server
    from trame_slicer.views import SliceView
    from vtk import vtkRenderWindowInteractor


class MyInteractor(BaseCustomVSelectLogic[SingleTouchFunctionsEnum]):
    def __init__(self, server: Server, slicer_app: SlicerApp, slice_view: SliceView):
        super().__init__(server, slicer_app, SingleTouchFunctionsState)
        self._slice_view = slice_view

        self._is_dragging = False
        self._first_drag = (0, 0)
        self._last_drag = (0, 0)

        self._first_scale = 1
        self._last_scale = 1

        self._first_pan = (0, 0)
        self._last_pan = (0, 0)

        self._first_slice = 0

        self._first_windowlevel = (0, 0)

        interaction_mapping = [
            ["MouseMoveEvent", self.on_drag],
            ["LeftButtonPressEvent", self.on_button_press],
            ["LeftButtonReleaseEvent", self.on_button_release],
            ["StartPanEvent",self.on_start_pan],
            ["PanEvent", self.on_pan],
            ["EndPanEvent", self.on_end_pan],
            ["StartRotateEvent", self.on_start_rotate],
            ["RotateEvent", self.on_rotate],
            ["EndRotateEvent", self.on_end_rotate]
        ]

        for event, callback in interaction_mapping:
            # self.interactor.RemoveObservers(event)
            self.interactor.AddObserver(event, callback, 1.0)

    def on_button_press(self, _obj: Any, _event: Any) -> None:
        self._is_dragging = True
        self._first_drag = self.interactor.GetEventPosition()
        self._last_drag = self._first_drag

        if self.is_selected(SingleTouchFunctionsEnum.SLICE):
            self._first_slice = self._slice_view.get_slice_value()
        
        if self.is_selected(SingleTouchFunctionsEnum.CONTRAST):
            min, max = VolumeWindowLevel.get_volume_display_range(self._slice_view.get_volume_layer_logic().GetVolumeNode())
            self._first_windowlevel = VolumeWindowLevel.min_max_to_window_level(min, max)

    def on_button_release(self, _obj: Any, _event: Any) -> None:
        self._is_dragging = False

    def on_drag(self, _obj: Any, _event: Any) -> None:
        x, y = self.interactor.GetEventPosition()
        if self._is_dragging:
            delta_x = x - self._first_drag[0]
            delta_y = y - self._first_drag[1]
            dx = x - self._last_drag[0]
            dy = y - self._last_drag[1]
            self._last_drag = (x, y)

            if self.is_selected(SingleTouchFunctionsEnum.ZOOM):
                zoom_speed = 0.001
                self._zoom(self._slice_view, exp(zoom_speed * dy))
            
            if self.is_selected(SingleTouchFunctionsEnum.SLICE):
                slice_change_speed = 0.03
                delta_slice = int(delta_y * slice_change_speed)
                min_slice, max_slice = self._slice_view.get_slice_range()
                self._slice_view.set_slice_value(max(min_slice, min(self._first_slice + delta_slice, max_slice)))

            if self.is_selected(SingleTouchFunctionsEnum.PAN):
                self._translate((dx, dy))
            
            if self.is_selected(SingleTouchFunctionsEnum.CONTRAST):
                delta_window_level = [delta_x , delta_y * 0.4]
                new_window = max(0, self._first_windowlevel[0] + delta_window_level[0])
                new_level = self._first_windowlevel[1] + delta_window_level[1]
                VolumeWindowLevel.set_volume_node_window_level(self._slice_view.get_volume_layer_logic().GetVolumeNode(), new_window, new_level)
                self._slice_view.schedule_render()

    def on_start_pan(self, _obj: Any, _event: Any) -> None:
        x, y = self.interactor.GetEventPosition()
        self._first_pan = (x,y)
        self._last_pan = self._first_pan


    def on_pan(self, _obj: Any, _event: Any) -> None:
        x, y = self.interactor.GetEventPosition()
        _delta_x = x - self._first_pan[0]
        _delta_y = y - self._first_pan[1]
        dx = x - self._last_pan[0]
        dy = y - self._last_pan[1]
        self._last_pan = (x, y)

        self._translate((dx, dy))

    def on_end_pan(self, _obj: Any, _event: Any) -> None:
        pass

    def on_start_rotate(self, _obj: Any, _event: Any) -> None:
        pass

    def on_rotate(self, _obj: Any, _event: Any) -> None:
        pass

    def on_end_rotate(self, _obj: Any, _event: Any) -> None:
        pass

    def _translate(self, translation: tuple[float, float]) -> None:
        dx, dy = translation
        fov_x, fov_y, _ = self._slice_view.get_view_node().GetFieldOfView()
        dims = self._slice_view.render_window().GetSize()

        scale_x = fov_x / dims[0]
        scale_y = fov_y / dims[1]

        origin = list(self._slice_view.get_view_node().GetXYZOrigin())
        origin[0] -= dx * scale_x
        origin[1] -= dy * scale_y

        self._slice_view.get_view_node().SetXYZOrigin(*origin)
        self._slice_view.schedule_render()
    
    # scale around 1
    def _zoom(self, view: SliceView, scale: float) -> None:
        view.zoom(log(scale))

    @property
    def interactor(self) -> vtkRenderWindowInteractor:
        return self._slice_view.interactor()

    def set_single_touch_function_none(self) -> None:
        self.data.selected = SingleTouchFunctionsEnum.NONE

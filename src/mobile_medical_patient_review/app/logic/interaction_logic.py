from math import exp, log

from slicer import vtkMRMLVolumeNode
from trame_server import Server
from trame_slicer.core import SlicerApp, VolumeWindowLevel
from trame_slicer.views.slice_view import SliceView

from ..ui.single_touch_functions_ui import (
    SingleTouchFunctionsEnum,
    SingleTouchFunctionsState,
)
from .base.base_custom_vselect_logic import BaseCustomVSelectLogic
from .interaction_observer import InteractionObserver


class InteractionLogic(BaseCustomVSelectLogic[SingleTouchFunctionsEnum], InteractionObserver):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, SingleTouchFunctionsState)
        self._begin_slice = {}
        self._begin_windowlevel = {}

    def get_volume_node(self, view: SliceView) -> vtkMRMLVolumeNode:
        return view.get_volume_layer_logic().GetVolumeNode()
    
    def on_start_drag(self, view: SliceView) -> None:
        if self.is_selected(SingleTouchFunctionsEnum.SLICE):
            self._begin_slice[view] = view.get_slice_value()
        
        if self.is_selected(SingleTouchFunctionsEnum.CONTRAST):
            min, max = VolumeWindowLevel.get_volume_display_range(self.get_volume_node(view))
            self._begin_windowlevel[view] = VolumeWindowLevel.min_max_to_window_level(min, max)
        
    def on_drag(self, view: SliceView, dx: float, dy: float, delta_x: float, delta_y: float) -> None:
        if self.is_selected(SingleTouchFunctionsEnum.ZOOM):
            zoom_speed = 0.001
            self._zoom(view, exp(zoom_speed * dy))
        
        if self.is_selected(SingleTouchFunctionsEnum.SLICE):
            slice_change_speed = 0.03
            delta_slice = int(delta_y * slice_change_speed)
            min_slice, max_slice = view.get_slice_range()
            view.set_slice_value(max(min_slice, min(self._begin_slice[view] + delta_slice, max_slice)))

        if self.is_selected(SingleTouchFunctionsEnum.PAN):
            self._translate(view, (dx, dy))
        
        if self.is_selected(SingleTouchFunctionsEnum.CONTRAST):
            delta_window_level = [delta_x * 0.5, delta_y * 0.2]
            new_window = max(0, self._begin_windowlevel[view][0] + delta_window_level[0])
            new_level = self._begin_windowlevel[view][1] + delta_window_level[1]
            VolumeWindowLevel.set_volume_node_window_level(self.get_volume_node(view), new_window, new_level)
            view.schedule_render()

    def on_end_drag(self, view: SliceView) -> None:
        pass

    def on_start_pinch(self, view: SliceView) -> None:
        pass
    
    def on_pinch(self, view: SliceView, dscale: float, _delta_scale: float) -> None:
        self._zoom(view, dscale)

    def on_end_pinch(self, view: SliceView, dscale: float, _delta_scale: float) -> None:
        pass

    def on_start_pan(self, view: SliceView, dtranslation: tuple[float, float], _delta_translation: tuple[float, float]) -> None:
        pass

    def on_pan(self, view: SliceView, dtranslation: tuple[float, float], _delta_translation: tuple[float, float]) -> None:
        self._translate(view, dtranslation)

    def on_end_pan(self, view: SliceView, dtranslation: tuple[float, float], _delta_translation: tuple[float, float]) -> None:
        pass

    def on_start_rotate(self, view: SliceView, drotation: tuple[float, float], delta_rotation: tuple[float, float]) -> None:
        pass

    def on_rotate(self, view: SliceView, drotation: tuple[float, float], delta_rotation: tuple[float, float]) -> None:
        pass

    def on_end_rotate(self, view: SliceView, drotation: tuple[float, float], delta_rotation: tuple[float, float]) -> None:
        pass

    def _translate(self, view: SliceView, translation: tuple[float, float]) -> None:
        dx, dy = translation
        fov_x, fov_y, _ = view.get_view_node().GetFieldOfView()
        dims = view.render_window().GetSize()

        scale_x = fov_x / dims[0]
        scale_y = fov_y / dims[1]

        origin = list(view.get_view_node().GetXYZOrigin())
        origin[0] -= dx * scale_x
        origin[1] -= dy * scale_y

        view.get_view_node().SetXYZOrigin(*origin)
        view.schedule_render()
    
    # scale around 1
    def _zoom(self, view: SliceView, scale: float) -> None:
        view.zoom(log(scale))

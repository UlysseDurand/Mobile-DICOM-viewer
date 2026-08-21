from trame_server import Server
from trame_slicer.core import LayoutManager, SlicerApp
from trame_slicer.rca_view import register_rca_factories
from trame_slicer.views import Layout, LayoutDirection, ViewLayoutDefinition

from ..ui.menus.annotator_menu_ui import AnnotatorMenuUI
from ..ui.menus.volume_menu_ui import VolumeMenuUI
from ..ui.mobile_medical_review_ui import MobileMedicalReviewUI
from ..ui.view_slicer_nb_ui import create_slice_nb_view_ui
from .menus.annotation_tool_menu_logic import AnnotationToolMenuLogic
from .menus.volume_menu_logic import VolumeMenuLogic
from .my_interactor import MyInteractor


class MobileMedicalReviewLogic:
    def __init__(self, server: Server, slicer_app: SlicerApp) -> None:
        self._server = server
        self._slicer_app = slicer_app

        register_rca_factories(
            self._slicer_app.view_manager,
            self._server,
            slice_view_ui_f=create_slice_nb_view_ui,
        )

        self._layout_manager = LayoutManager(self._slicer_app.scene, self._slicer_app.view_manager, self._server)
        self._layout_manager.register_layout_dict({"Axial Only": Layout(LayoutDirection.Vertical, [ViewLayoutDefinition.axial_view()])})
        self._layout_manager.set_layout("Axial Only")

        self._volume_menu_logic = VolumeMenuLogic(server, slicer_app)
        self._annotation_tool_menu_logic = AnnotationToolMenuLogic(server, slicer_app)

        self._interactor_observers = {}
        for view in self._slicer_app.view_manager.get_slice_views():
            self._interactor_observers[view.get_view_node_id()] = MyInteractor(server, slicer_app, view)

        for interactor in self._interactor_observers.values():
            self._annotation_tool_menu_logic.set_single_touch_function(
                interactor.set_single_touch_function_none
            )
            interactor.set_deselect_markup_callback(self._annotation_tool_menu_logic.deselect_tool)

    def set_ui(self, ui: MobileMedicalReviewUI) -> None:
        self._volume_menu_logic.set_ui(ui.main_menu_selector_ui.get_menu_ui(VolumeMenuUI))
        self._annotation_tool_menu_logic.set_ui(ui.main_menu_selector_ui.get_menu_ui(AnnotatorMenuUI).tool_menu)

    @property
    def layout_manager(self) -> LayoutManager:
        return self._layout_manager

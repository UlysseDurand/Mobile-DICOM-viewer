from trame_server import Server
from trame_slicer.core import LayoutManager, SlicerApp
from trame_slicer.rca_view import register_rca_factories
from trame_slicer.views import Layout, LayoutDirection, ViewLayoutDefinition
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch
from .my_interactor_style import MyInteractorStyle

from ..ui.menus.volume_menu_ui import VolumeMenuUI
from ..ui.mobile_medical_review_ui import MobileMedicalReviewUI
from ..ui.view_slicer_nb_ui import create_slice_nb_view_ui
from .menus.volume_menu_logic import VolumeMenuLogic
from .interaction_logic import InteractionLogic

class MobileMedicalReviewLogic:
    def __init__(self, server: Server, slicer_app: SlicerApp) -> None:
        self._server = server
        self._slicer_app = slicer_app

        register_rca_factories(
            self._slicer_app.view_manager, 
            self._server, 
            slice_view_ui_f=create_slice_nb_view_ui
        )

        self._layout_manager = LayoutManager(self._slicer_app.scene, self._slicer_app.view_manager, self._server)
        self._layout_manager.register_layout_dict({"Axial Only": Layout(LayoutDirection.Vertical, [ViewLayoutDefinition.axial_view()])})
        self._layout_manager.set_layout("Axial Only")

        self._interaction_logic = InteractionLogic(server, slicer_app)
        self._volume_menu_logic = VolumeMenuLogic(server, slicer_app)

        for view in self._slicer_app.view_manager.get_views():
            interactor_style = MyInteractorStyle(view) 
            interactor_style.add_interaction_observer(self._interaction_logic)
            view.interactor().SetInteractorStyle(interactor_style)

    def set_ui(self, ui: MobileMedicalReviewUI) -> None:
        self._volume_menu_logic.set_ui(ui.main_menu_selector_ui.get_menu_ui(VolumeMenuUI))

    @property
    def layout_manager(self) -> LayoutManager:
        return self._layout_manager
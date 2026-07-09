from trame_server import Server
from trame_slicer.core import LayoutManager

from .main_menu_selector_ui import MainMenuSelectorUI
from .mobile_viewer_layout import MobileViewerLayout
from .single_touch_functions_ui import SingleTouchFunctionsUI


class MobileMedicalReviewUI:
    def __init__(self, server: Server, layout_manager: LayoutManager):
        server.state.trame__title = "Mobile medical patient review"

        with MobileViewerLayout(server) as self.layout:
            self.layout.right_icon.icon = "mdi-file-document"
            with self.layout.toolbar:
                self.single_touch_functions_ui = SingleTouchFunctionsUI()
            
            with self.layout.left_drawer:
                self.main_menu_selector_ui = MainMenuSelectorUI()
            
            with self.layout.content:
                layout_manager.initialize_layout_grid(self.layout)
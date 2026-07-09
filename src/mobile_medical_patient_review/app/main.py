from trame.app import TrameApp
from trame_server import Server
from trame_slicer.core import SlicerApp

from .logic.mobile_medical_review_logic import MobileMedicalReviewLogic
from .ui.mobile_medical_review_ui import MobileMedicalReviewUI


class MobileMedicalReviewApp(TrameApp):
    def __init__(self, server: Server=None) -> None:
        super().__init__(server)
        self._slicer_app = SlicerApp()
        self._logic = MobileMedicalReviewLogic(self.server, self._slicer_app)
        self._ui = MobileMedicalReviewUI(self.server, self._logic.layout_manager)
        self._logic.set_ui(self._ui)

def main(server: Server=None, **kwargs: dict) -> None:
    app = MobileMedicalReviewApp(server)
    app.server.start(**kwargs)

if __name__ == "__main__":
    main()

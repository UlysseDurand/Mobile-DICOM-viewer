import os
from pathlib import Path

from trame_server import Server
from trame_slicer.app.logic import BaseLogic
from trame_slicer.core import SlicerApp

from ...ui.menus.volume_menu_ui import VolumeMenuState, VolumeMenuUI


class VolumeMenuLogic(BaseLogic[VolumeMenuState]):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, VolumeMenuState)
        self.data.available_volumes = self._get_volumes()
        self.active_volume = None

    def _get_volumes(self) -> list[str]:
        with os.scandir("volumes") as entries:
            return [entry.name for entry in entries]
    
    def _get_files(self, volume: str) -> list[str]:
        dir_path = Path("volumes") / volume
        return [str(file) for file in dir_path.iterdir()]
        
    def _load_volume(self, volume: str) -> None:
        files = self._get_files(volume)
        self._slicer_app.scene.Clear()
        volumes = self._slicer_app.io_manager.load_volumes(files)
        self.active_volume = volumes[0]
        self._slicer_app.display_manager.show_volume(self.active_volume, do_reset_views=True)

    def set_ui(self, ui: VolumeMenuUI) -> None:
        ui.load_volume.connect(self._load_volume)
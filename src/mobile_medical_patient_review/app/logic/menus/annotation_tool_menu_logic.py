from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from trame_slicer.app.logic import BaseLogic

from ...ui.menus.annotation_tool_menus.annotation_tool_menu_ui import (
    AnnotationComment,
    AnnotationToolMenuState,
)

MARKUP_DISPLAY_GLYPH_SCALE = 10.0
MARKUP_DISPLAY_TEXT_SCALE = 5.0

if TYPE_CHECKING:
    from collections.abc import Callable

    from trame_server import Server
    from trame_slicer.core import SlicerApp

    from ...ui.comments_ui import CommentsUI
    from ...ui.menus.annotation_tool_menus.annotation_tool_menu_ui import (
        AnnotationToolMenuUI,
    )


class AnnotationToolMenuLogic(BaseLogic[AnnotationToolMenuState]):
    _TOOL_MAP: ClassVar[dict[str, tuple[str, bool]]] = {
        "FiducialToolMenuUI": ("vtkMRMLMarkupsFiducialNode", True),
        "RulerToolMenuUI": ("vtkMRMLMarkupsLineNode", False),
        "AngleToolMenuUI": ("vtkMRMLMarkupsAngleNode", False),
        "OpenCurveToolMenuUI": ("vtkMRMLMarkupsCurveNode", True),
        "ClosedCurveToolMenuUI": ("vtkMRMLMarkupsClosedCurveNode", True),
        "PlaneToolMenuUI": ("vtkMRMLMarkupsPlaneNode", False),
        "RoiToolMenuUI": ("vtkMRMLMarkupsROINode", False),
    }

    _NODE_META: ClassVar[dict[str, tuple[str, str]]] = {
        "vtkMRMLMarkupsFiducialNode": ("Fiducial", "mdi-circle-small"),
        "vtkMRMLMarkupsLineNode": ("Ruler", "mdi-ruler"),
        "vtkMRMLMarkupsAngleNode": ("Angle", "mdi-angle-acute"),
        "vtkMRMLMarkupsCurveNode": ("Open Curve", "mdi-vector-polyline"),
        "vtkMRMLMarkupsClosedCurveNode": ("Closed Curve", "mdi-vector-polygon"),
        "vtkMRMLMarkupsPlaneNode": ("Plane", "mdi-square-outline"),
        "vtkMRMLMarkupsROINode": ("ROI", "mdi-cube-outline"),
    }

    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, AnnotationToolMenuState)
        self._markup_nodes: list = []
        self._single_touch_function_cb: Callable[[], None] | None = None

    def set_single_touch_function(self, callback: Callable[[], None]) -> None:
        self._single_touch_function_cb = callback

    def deselect_tool(self) -> None:
        if self.data.selected is not None:
            self.data.selected = None

    def set_ui(self, tool_menu: AnnotationToolMenuUI, comments_ui: CommentsUI) -> None:
        self.bind_changes({self.name.selected: self._on_tool_changed})
        tool_menu.clear_clicked.connect(self._on_clear)
        comments_ui.comment_changed.connect(self._on_comment_changed)

    def _on_tool_changed(self, selected: str | None) -> None:
        self._slicer_app.markups_logic.disable_place_mode()
        if selected is None or selected not in self._TOOL_MAP:
            return
        node_type, persistent = self._TOOL_MAP[selected]
        node = self._slicer_app.scene.AddNewNodeByClass(node_type)
        if node is not None:
            self._markup_nodes.append(node)
            self._slicer_app.markups_logic.place_node(node, persistent)
            self._set_markup_display_properties(node)
            self._add_annotation(node)
            if self._single_touch_function_cb is not None:
                self._single_touch_function_cb()

    def _set_markup_display_properties(self, node: Any) -> None:
        if node.GetDisplayNode() is None:
            node.CreateDefaultDisplayNodes()
        display = node.GetDisplayNode()
        display.SetGlyphScale(MARKUP_DISPLAY_GLYPH_SCALE)
        display.SetTextScale(MARKUP_DISPLAY_TEXT_SCALE)

    def _add_annotation(self, node: Any) -> None:
        label, icon = self._NODE_META.get(node.GetClassName(), ("Annotation", "mdi-tag"))
        annotation = AnnotationComment(
            node_id=node.GetID(),
            name=node.GetName(),
            type_label=label,
            icon=icon,
        )
        self.data.annotations = [*self.data.annotations, annotation]

    def _on_comment_changed(self, node_id: str, comment: str) -> None:
        node = self._slicer_app.scene.GetNodeByID(node_id)
        if node is not None:
            node.SetDescription(comment)

    def _on_clear(self) -> None:
        self._slicer_app.markups_logic.disable_place_mode()
        for node in self._markup_nodes:
            self._slicer_app.scene.RemoveNode(node)
        self._markup_nodes.clear()
        self.data.annotations = []

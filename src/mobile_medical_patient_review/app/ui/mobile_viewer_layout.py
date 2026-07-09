from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.html import Template
from trame.widgets.vuetify3 import VBtn, VNavigationDrawer
from trame_server import Server


class MobileViewerLayout(SinglePageLayout):
    def __init__(self, server: Server):
        super().__init__(server)
        with self:
            self.title.set_text("")
            with self.toolbar:
                with Template(v_slot_append=""):
                    self.right_icon = VBtn(icon="mdi-dots-vertical")

            
            self.left_drawer = VNavigationDrawer(
                temporary=True,
                location="left",
                v_model=("left_drawer", False),
                width=400,
            )
            self.icon.click = "left_drawer = !left_drawer; if (left_drawer && right_drawer) {right_drawer = false;}"

            self.right_drawer = VNavigationDrawer(
                temporary=True,
                location="right",
                v_model=("right_drawer", False),
                width=400,
            ) 
            self.right_icon.click = "right_drawer = !right_drawer; if (left_drawer && right_drawer) {left_drawer = false;}"
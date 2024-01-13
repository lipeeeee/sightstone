# Module that handles gui

import string
import random
import dearpygui.dearpygui as dpg
from sightstone import Sightstone

WIDTH = 500
HEIGHT = 400

def init_gui(sightstone_hook: Sightstone):
    """Inits dearpygui window"""
    dpg.create_context()

    with dpg.window(
            label="sightstone",
            width=WIDTH, height=HEIGHT,
            no_resize=True, no_title_bar=True, tag="p1"
        ):
        with dpg.tab_bar():
            with dpg.tab(label="Client"):
                dpg.add_button(label="Remove Challenges",
                               callback=sightstone_hook.remove_challenges)
            with dpg.tab(label="Queue"):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
        with dpg.colormap_registry(label="Colormap Registry", show=False):
            dpg.add_colormap([[255, 255, 255, 255], [255, 255, 255, 255]], True, tag="white", label="white")
        dpg.add_text("INFO TEXT", tag="info", pos=(WIDTH // 2 - 80, HEIGHT - 75))

    dpg.set_primary_window("p1", True)

    # safe title for riot detection sake
    letter_dict = string.ascii_letters + string.digits + string.punctuation
    safe_title = "".join(random.choice(letter_dict) for _ in range(20))
    dpg.create_viewport(
        title=safe_title,
        width=WIDTH, height=HEIGHT,
        resizable=False
    )
    dpg.show_viewport()

    dpg.setup_dearpygui()
    while dpg.is_dearpygui_running():
        # Update necessary info for each frame
        connected_string = "CONNECTED TO CLIENT" if sightstone_hook.lca_hook.connected else "NOT CONNECTED TO CLIENT"
        dpg.set_value("info", connected_string)

        dpg.render_dearpygui_frame()
    dpg.destroy_context()

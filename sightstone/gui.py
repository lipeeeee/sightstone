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
                dpg.add_button(label="Remove Challenges", callback=sightstone_hook.remove_challenges)
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
        dpg.render_dearpygui_frame()
    dpg.destroy_context()

# Module that handles gui

import string
import random
import dearpygui.dearpygui as dpg
from sightstone import Sightstone

WIDTH = 500
HEIGHT = 400

INFO_LABEL_TEXT = "Sightstone by lipeeeee, "

def init_gui(sightstone_hook: Sightstone):
    """Inits dearpygui window"""
    dpg.create_context()

    with dpg.window(
            label="sightstone",
            width=WIDTH, height=HEIGHT,
            no_resize=True, no_title_bar=True, tag="p1"
        ):
        #dpg.add_text("", tag="info")
        dpg.add_text("", tag="info", pos=(10, HEIGHT - 75))
        with dpg.tab_bar():
            with dpg.tab(label="Game"):
                pass
            with dpg.tab(label="Profile"):
                dpg.add_button(label="Remove Challenges",
                               callback=sightstone_hook.remove_challenges)
            with dpg.tab(label="Info"):
                pass
            with dpg.tab(label="Champs"):
                pass
            with dpg.tab(label="Skins"):
                pass
            with dpg.tab(label="Misc"):
                pass
            with dpg.tab(label="Custom"):
                pass
            with dpg.tab(label="Settings"):
                pass
            with dpg.tab(label="Test"):
                dpg.add_button(label="gamemodes",
                               callback=sightstone_hook.get_queues)
                dpg.add_button(label="create arurf",
                               callback=lambda:sightstone_hook.create_lobby("450"))
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
        dpg.set_value("info", INFO_LABEL_TEXT + connected_string)

        dpg.render_dearpygui_frame()
    dpg.destroy_context()

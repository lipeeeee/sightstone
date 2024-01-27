# Module that handles gui

import string
import random
import dearpygui.dearpygui as dpg
import sightstone_constants as SC
from sightstone import Sightstone

WIDTH = 600
HEIGHT = 400

INFO_LABEL_TEXT = SC.SIGHTSTONE + " by lipeeeee, "
IDENT_BUTTONS_GROUP_4 = WIDTH // 4

def init_gui(sightstone_hook: Sightstone):
    """Inits dearpygui window"""
    dpg.create_context()

    with dpg.window(
            label=SC.SIGHTSTONE,
            width=WIDTH, height=HEIGHT,
            no_resize=True, no_title_bar=True, tag="p1"
        ):
        #dpg.add_text("", tag="info", pos=(10, HEIGHT - 75))
        dpg.add_text("", tag="info")
        with dpg.tab_bar():
            with dpg.tab(label="Game"):
                dpg.add_text("Create lobby")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Quick Play",
                                    callback=lambda:sightstone_hook.create_lobby(SC.QUICK_PLAY_ID))
                    dpg.add_button(label="ARAM",
                                    callback=lambda:sightstone_hook.create_lobby(SC.ARAM_PLAY_ID),
                                    indent=IDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Normal",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_NORMAL_ID),
                                    indent=IDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="TFT Tutorial",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_TUTORIAL_ID),
                                    indent=(IDENT_BUTTONS_GROUP_4 * 2) + IDENT_BUTTONS_GROUP_4)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Draft Pick",
                                    callback=lambda:sightstone_hook.create_lobby(SC.DRAFT_PICK_ID))
                    dpg.add_button(label="ARURF",
                                    callback=lambda:sightstone_hook.create_lobby(SC.ARURF_ID),
                                    indent=IDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Ranked",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_RANKED_ID),
                                    indent=IDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="Practi. Tool",
                                    callback=lambda:sightstone_hook.create_lobby("0", custom=SC.PRACT_TOOL_JSON),
                                    indent=(IDENT_BUTTONS_GROUP_4 * 2) + IDENT_BUTTONS_GROUP_4)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Solo/Duo",
                                    callback=lambda:sightstone_hook.create_lobby(SC.SOLO_DUO_ID))
                    dpg.add_button(label="ARURF 1v1",
                                    callback=lambda:sightstone_hook.create_lobby(SC.ARURF_1V1_ID),
                                    indent=IDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Hyper Roll",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_HYPERROLL_ID),
                                    indent=IDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="Practi. Tool 5v5",
                                    callback=lambda:sightstone_hook.create_lobby("0", custom=SC.PRACT_TOOL_5V5_JSON),
                                    indent=(IDENT_BUTTONS_GROUP_4 * 2) + IDENT_BUTTONS_GROUP_4)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Flex",
                                    callback=lambda:sightstone_hook.create_lobby(SC.FLEX_PLAY_ID))
                    dpg.add_button(label="Nexus Blitz",
                                    callback=lambda:sightstone_hook.create_lobby(SC.NEXUS_BLITZ_ID),
                                    indent=IDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Double Up",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_DOUBLE_UP_ID),
                                    indent=IDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="Clash",
                                    callback=lambda:sightstone_hook.create_lobby(SC.CLASH_ID),
                                    indent=(IDENT_BUTTONS_GROUP_4 * 2) + IDENT_BUTTONS_GROUP_4)
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
                dpg.add_button(label="pos",
                                callback=lambda:sightstone_hook.set_positions(
                                sightstone_hook.ROLE_TO_INT_MAPPING[dpg.get_value("pos1")], 
                                sightstone_hook.ROLE_TO_INT_MAPPING[dpg.get_value("pos2")]))
                dpg.add_combo(tag="pos1", 
                                items=list(sightstone_hook.ROLE_TO_INT_MAPPING.keys()),
                                callback=lambda:sightstone_hook.set_positions(
                                sightstone_hook.ROLE_TO_INT_MAPPING[dpg.get_value("pos1")], 
                                sightstone_hook.ROLE_TO_INT_MAPPING[dpg.get_value("pos2")]))
                dpg.add_combo(tag="pos2", 
                                items=list(sightstone_hook.ROLE_TO_INT_MAPPING.keys()),
                                callback=lambda:sightstone_hook.set_positions(
                                sightstone_hook.ROLE_TO_INT_MAPPING[dpg.get_value("pos1")], 
                                sightstone_hook.ROLE_TO_INT_MAPPING[dpg.get_value("pos2")]))
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

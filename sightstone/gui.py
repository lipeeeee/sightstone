# Module that handles gui

import string
import random
import dearpygui.dearpygui as dpg
import sightstone_constants as SC
from sightstone import Sightstone

WIDTH = 600
HEIGHT = 400

INDENT_BUTTONS_GROUP_4 = WIDTH // 4

"""Role to int mapping"""
ROLE_TO_INT_MAPPING = {
    "TOP":  "0",
    "JGL":  "1",
    "MID":  "2",
    "ADC":  "3",
    "SUP":  "4",
    "FILL": "5",
    "NONE": "6",
    "":     "6",
}

"""Difficulty to int mapping"""
DIFFICULTY_TO_INT_MAPPING = {
    "NONE":     "0",
    "EASY":     "1",
    "MEDIUM":   "2",
    "HARD":     "3",
    "UBER":     "4",
    "TUTORIAL": "5",
    "INTRO":    "6",
}

def info_label(sightstone_hook: Sightstone):
    """Returns info label(top label) with sightstone info"""
    info = SC.SIGHTSTONE + " by lipeeeee" # General info
    info += " - " + sightstone_hook.get_current_patch() # Patch info
    info += " | Connected to: " + str(sightstone_hook.get_current_user()) # User info
    return info

# pylint: disable=R0915
def init_gui(sightstone_hook: Sightstone):
    """Inits dearpygui window"""
    dpg.create_context()

    with dpg.window(
            label=SC.SIGHTSTONE,
            width=WIDTH, height=HEIGHT,
            no_resize=True, no_title_bar=True, tag="p1"
        ):
        dpg.add_text("", tag="info")
        with dpg.tab_bar():
            with dpg.tab(label="Game"):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Quick Play",
                                    callback=lambda:sightstone_hook.create_lobby(SC.QUICK_PLAY_ID))
                    dpg.add_button(label="ARAM",
                                    callback=lambda:sightstone_hook.create_lobby(SC.ARAM_PLAY_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Normal",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_NORMAL_ID),
                                    indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="TFT Tutorial",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_TUTORIAL_ID),
                                    indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Draft Pick",
                                    callback=lambda:sightstone_hook.create_lobby(SC.DRAFT_PICK_ID))
                    dpg.add_button(label="ARURF",
                                    callback=lambda:sightstone_hook.create_lobby(SC.ARURF_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Ranked",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_RANKED_ID),
                                    indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="Practi. Tool",
                                    callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.PRACTICE_TOOL_MODE, 1, SC.SUMMONERS_RIFT_ID)),
                                    indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Solo/Duo",
                                    callback=lambda:sightstone_hook.create_lobby(SC.SOLO_DUO_ID))
                    dpg.add_button(label="ARURF 1v1",
                                    callback=lambda:sightstone_hook.create_lobby(SC.ARURF_1V1_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Hyper Roll",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_HYPERROLL_ID),
                                    indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="Practi. Tool 5v5",
                                    callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.PRACTICE_TOOL_MODE, 5, SC.SUMMONERS_RIFT_ID)),
                                    indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Flex",
                                    callback=lambda:sightstone_hook.create_lobby(SC.FLEX_PLAY_ID))
                    dpg.add_button(label="Nexus Blitz",
                                    callback=lambda:sightstone_hook.create_lobby(SC.NEXUS_BLITZ_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="TFT Double Up",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TFT_DOUBLE_UP_ID),
                                    indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(label="Clash",
                                    callback=lambda:sightstone_hook.create_lobby(SC.CLASH_ID),
                                    indent=INDENT_BUTTONS_GROUP_4 * 3)

                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Tutorial 1",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TUTORIAL_1_ID))
                    dpg.add_button(label="Intro Bots",
                                    callback=lambda:sightstone_hook.create_lobby(SC.INTRO_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="Custom Blind",
                                    callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.CLASSIC_MODE, 5, SC.SUMMONERS_RIFT_ID)),
                                    indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_combo(tag="create_mapId",
                                    width=100, items=list(SC.STR_TO_MAP.keys()),
                                    indent=INDENT_BUTTONS_GROUP_4 * 3) 

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Tutorial 2",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TUTORIAL_2_ID))
                    dpg.add_button(label="Begginer Bots",
                                    callback=lambda:sightstone_hook.create_lobby(SC.BEGGINER_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="Custom ARAM",
                                    callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.CLASSIC_MODE, 5, SC.HOWLING_ABYSS_ID)),
                                    indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_combo(tag="create_teamCount",
                                    width=100, items=[str(i) for i in range(1, 6)],
                                    indent=INDENT_BUTTONS_GROUP_4 * 3) 

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Tutorial 3",
                                    callback=lambda:sightstone_hook.create_lobby(SC.TUTORIAL_3_ID))
                    dpg.add_button(label="Intermediate Bots",
                                    callback=lambda:sightstone_hook.create_lobby(SC.INTERMEDIATE_ID),
                                    indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(label="Create Custom",
                                    callback=lambda:sightstone_hook.create_lobby("0", 
                                                    custom=sightstone_hook.custom_game_json(SC.CLASSIC_MODE, dpg.get_value("create_teamCount"), SC.STR_TO_MAP[dpg.get_value("create_mapId")])),
                                    indent=INDENT_BUTTONS_GROUP_4 * 3)

                dpg.add_separator()
                with dpg.group(horizontal=True):
                    ...

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
                                ROLE_TO_INT_MAPPING[dpg.get_value("pos1")],
                                ROLE_TO_INT_MAPPING[dpg.get_value("pos2")]))
                dpg.add_combo(tag="pos1",
                                items=list(ROLE_TO_INT_MAPPING.keys()),
                                callback=lambda:sightstone_hook.set_positions(
                                ROLE_TO_INT_MAPPING[dpg.get_value("pos1")],
                                ROLE_TO_INT_MAPPING[dpg.get_value("pos2")]))
                dpg.add_combo(tag="pos2",
                                items=list(ROLE_TO_INT_MAPPING.keys()),
                                callback=lambda:sightstone_hook.set_positions(
                                ROLE_TO_INT_MAPPING[dpg.get_value("pos1")],
                                ROLE_TO_INT_MAPPING[dpg.get_value("pos2")]))
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
        dpg.set_value("info", info_label(sightstone_hook))

        dpg.render_dearpygui_frame()
    dpg.destroy_context()

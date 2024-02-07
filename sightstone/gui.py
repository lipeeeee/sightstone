# Module that handles gui

import string
import random
import dearpygui.dearpygui as dpg
from sightstone.background_thread import BackgroundThread
import sightstone.sightstone_constants as SC
from sightstone.sightstone import Sightstone

WIDTH = 600
HEIGHT = 500

INDENT_BUTTONS_GROUP_4 = WIDTH // 4

"""Role to int mapping"""
ROLE_TO_INT_MAPPING = {
    "TOP":  SC.TOP_ID,
    "JGL":  SC.JGL_ID,
    "MID":  SC.MID_ID,
    "ADC":  SC.ADC_ID,
    "SUP":  SC.SUP_ID,
    "FILL": SC.FILL_ID,
    "NONE": SC.NONE_ID,
}

"""Availability items"""
AVAILABILITY_ITEMS = [SC.ONLINE_AVAILABILITY, SC.AWAY_AVAILABILITY, SC.MOBILE_AVAILABILITY, SC.OFFLINE_AVAILABILITY]

"""Ranks"""
RANK_ITEMS = {
    "Iron": SC.IRON_RANK,
    "Bronze": SC.BRONZE_RANK,
    "Silver": SC.SILVER_RANK,
    "Gold": SC.GOLD_RANK,
    "Platinum": SC.PLATINUM_RANK,
    "Emerald": SC.EMERALD_RANK,
    "Diamond": SC.DIAMOND_RANK,
    "Master": SC.MASTER_RANK,
    "GrandMaster": SC.GRANDMASTER_RANK,
    "Challenger": SC.CHALLENGER_RANK
}
QUEUE_ITEMS = {
    "Solo/Duo": SC.SOLODUO_QUEUE_CODE,
    "Flex 5v5": SC.FLEX_QUEUE_CODE,
    "Twisted Treeline 3v3": SC.TWISTED_TREELINE_QUEUE_CODE,
    "TFT": SC.TFT_QUEUE_CODE,
    "Hyper Roll": SC.TFT_TURBO_QUEUE_CODE,
    "Double Up": SC.TFT_DOUBLE_UP_QUEUE_CODE,
    "Arena": SC.ARENA_QUEUE_CODE,
    "None": str()
}
DIVISION_ITEMS = {
    "I": SC.DIVISION_I,
    "II": SC.DIVISION_II,
    "III": SC.DIVISION_III,
    "IV": SC.DIVISION_IV,
    "None": str()
}

INSTANT_GROUP_WIDTH = WIDTH - (WIDTH // 3)

"""Friend groups"""
friend_groups: list

### Threads
update_friend_groups_thread: BackgroundThread
UPDATE_FRIEND_GROUPS_TIMEOUT = 5
SLOW_UPDATE_FRIEND_GROUPS_TIMEOUT = 13
def update_friend_groups(sightstone_hook: Sightstone):
    """Threaded function to periodically update `friend_groups`"""
    if sightstone_hook.lca_hook.connected:
        update_friend_groups_thread.time_between_runs = SLOW_UPDATE_FRIEND_GROUPS_TIMEOUT
    else:
        update_friend_groups_thread.time_between_runs = UPDATE_FRIEND_GROUPS_TIMEOUT
    friend_groups = [group["name"] for group in sightstone_hook.get_groups()]
    dpg.configure_item("friendGroups", items=friend_groups)

update_info_label_thread: BackgroundThread
UPDATE_INFO_LABEL_TIMEOUT = 5
def update_info_label(sightstone_hook: Sightstone):
    """Threaded function to periodically update `info_label` with sightstone/LCA info"""
    info = SC.SIGHTSTONE + " by lipeeeee" # General info
    info += " - " + sightstone_hook.get_current_patch() # Patch info
    info += " | Connected to: " + str(sightstone_hook.get_current_user()) # User info
    dpg.set_value("info", info)

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
                    role_to_int_str_list = list(ROLE_TO_INT_MAPPING.keys())
                    callback_set_roles = lambda:sightstone_hook.set_positions(
                        ROLE_TO_INT_MAPPING[dpg.get_value("pos1")],
                        ROLE_TO_INT_MAPPING[dpg.get_value("pos2")],
                    )
                    dpg.add_button(label="Start Queue", callback=sightstone_hook.start_queue)
                    dpg.add_combo(
                        tag="pos1", items=role_to_int_str_list, 
                        default_value=role_to_int_str_list[0], width=115, 
                        callback=callback_set_roles, indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_combo(
                        tag="pos2", items=role_to_int_str_list,
                        default_value=role_to_int_str_list[1], width=115, callback=callback_set_roles)
                    dpg.add_button(label="Dodge", callback=sightstone_hook.dodge_lobby, indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Delete Lobby", callback=sightstone_hook.delete_lobby)
                    dpg.add_button(
                        label="Lobby Reveal",
                        indent=INDENT_BUTTONS_GROUP_4,
                        callback=lambda:sightstone_hook.search_lobby(dpg.get_value("revealWebsite")))
                    dpg.add_combo(tag="revealWebsite", width=139, items=sightstone_hook.AVAILABLE_WEBSITES, default_value=sightstone_hook.AVAILABLE_WEBSITES[0])
                    dpg.add_button(
                        label="Search Myself",
                        indent=INDENT_BUTTONS_GROUP_4 * 3,
                        callback=lambda:sightstone_hook.search_myself(SC.OP_GG))
                
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="Auto Accept", callback=sightstone_hook.toggle_accept_listener)
                    dpg.add_button(
                        label="Invite from group",
                        indent=INDENT_BUTTONS_GROUP_4,
                        callback=lambda:sightstone_hook.invite_friends_from_group(dpg.get_value("friendGroups")))
                    dpg.add_combo(tag="friendGroups", width=104)

                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_input_text(tag="instaMessage", width=INSTANT_GROUP_WIDTH)
                    dpg.add_checkbox(label="Instant Message")
                with dpg.group(horizontal=True):
                    dpg.add_combo(tag="instaLock", width=INSTANT_GROUP_WIDTH, default_value="notyet")
                    dpg.add_checkbox(label="Instant Pick")
                with dpg.group(horizontal=True):
                    dpg.add_combo(tag="instaBan", width=INSTANT_GROUP_WIDTH, default_value="notyet")
                    dpg.add_checkbox(label="Instant Ban")

                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Quick Play", callback=lambda:sightstone_hook.create_lobby(SC.QUICK_PLAY_ID))
                    dpg.add_button(
                        label="ARAM",
                        callback=lambda:sightstone_hook.create_lobby(SC.ARAM_PLAY_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="TFT Normal",
                        callback=lambda:sightstone_hook.create_lobby(SC.TFT_NORMAL_ID),
                        indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(
                        label="TFT Tutorial",
                        callback=lambda:sightstone_hook.create_lobby(SC.TFT_TUTORIAL_ID),
                        indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Draft Pick", callback=lambda:sightstone_hook.create_lobby(SC.DRAFT_PICK_ID))
                    dpg.add_button(
                        label="ARURF",
                        callback=lambda:sightstone_hook.create_lobby(SC.ARURF_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="TFT Ranked",
                        callback=lambda:sightstone_hook.create_lobby(SC.TFT_RANKED_ID),
                        indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(
                        label="Practi. Tool",
                        callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.PRACTICE_TOOL_MODE, 1, SC.SUMMONERS_RIFT_ID)),
                        indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Solo/Duo", callback=lambda:sightstone_hook.create_lobby(SC.SOLO_DUO_ID))
                    dpg.add_button(
                        label="ARURF 1v1",
                        callback=lambda:sightstone_hook.create_lobby(SC.ARURF_1V1_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="TFT Hyper Roll",
                        callback=lambda:sightstone_hook.create_lobby(SC.TFT_HYPERROLL_ID),
                        indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(
                        label="Practi. Tool 5v5",
                        callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.PRACTICE_TOOL_MODE, 5, SC.SUMMONERS_RIFT_ID)),
                        indent=INDENT_BUTTONS_GROUP_4 * 3)

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Flex",
                        callback=lambda:sightstone_hook.create_lobby(SC.FLEX_PLAY_ID))
                    dpg.add_button(
                        label="Nexus Blitz",
                        callback=lambda:sightstone_hook.create_lobby(SC.NEXUS_BLITZ_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="TFT Double Up",
                        callback=lambda:sightstone_hook.create_lobby(SC.TFT_DOUBLE_UP_ID),
                        indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_button(
                        label="Clash",
                        callback=lambda:sightstone_hook.create_lobby(SC.CLASH_ID),
                        indent=INDENT_BUTTONS_GROUP_4 * 3)

                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Tutorial 1",
                        callback=lambda:sightstone_hook.create_lobby(SC.TUTORIAL_1_ID))
                    dpg.add_button(
                        label="Intro Bots",
                        callback=lambda:sightstone_hook.create_lobby(SC.INTRO_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="Custom Blind",
                        callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.CLASSIC_MODE, 5, SC.SUMMONERS_RIFT_ID)),
                        indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_combo(
                        tag="create_mapId",
                        width=100, items=list(SC.STR_TO_MAP.keys()),
                        default_value=list(SC.STR_TO_MAP.keys())[0],
                        indent=INDENT_BUTTONS_GROUP_4 * 3) 

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Tutorial 2",
                        callback=lambda:sightstone_hook.create_lobby(SC.TUTORIAL_2_ID))
                    dpg.add_button(
                        label="Begginer Bots",
                        callback=lambda:sightstone_hook.create_lobby(SC.BEGGINER_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="Custom ARAM",
                        callback=lambda:sightstone_hook.create_lobby("0", custom=sightstone_hook.custom_game_json(SC.CLASSIC_MODE, 5, SC.HOWLING_ABYSS_ID)),
                        indent=INDENT_BUTTONS_GROUP_4 * 2)
                    dpg.add_combo(
                        tag="create_teamCount",
                        width=100, items=[str(i) for i in range(1, 6)],
                        default_value="1",
                        indent=INDENT_BUTTONS_GROUP_4 * 3) 

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Tutorial 3",
                        callback=lambda:sightstone_hook.create_lobby(SC.TUTORIAL_3_ID))
                    dpg.add_button(
                        label="Intermediate Bots",
                        callback=lambda:sightstone_hook.create_lobby(SC.INTERMEDIATE_ID),
                        indent=INDENT_BUTTONS_GROUP_4)
                    dpg.add_button(
                        label="Create Custom",
                        callback=lambda:sightstone_hook.create_lobby("0", 
                        custom=sightstone_hook.custom_game_json(SC.CLASSIC_MODE, dpg.get_value("create_teamCount"), SC.STR_TO_MAP[dpg.get_value("create_mapId")])),
                        indent=INDENT_BUTTONS_GROUP_4 * 3)

            with dpg.tab(label="Profile"):
                with dpg.group():
                    dpg.add_text("Status:")
                    dpg.add_input_text(tag="statusImportTxt", width=WIDTH - 30, height=100, multiline=True)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Import Status", callback=lambda:sightstone_hook.import_status_txt(dpg.get_value("statusImportTxt")))
                        dpg.add_radio_button(tag="statusAvailability", items=AVAILABILITY_ITEMS, horizontal=True, callback=lambda:sightstone_hook.import_status_availability(dpg.get_value("statusAvailability")))
                dpg.add_separator()

                with dpg.group():
                    dpg.add_text("Rank:")
                    with dpg.group(horizontal=True):
                        dpg.add_combo(tag="rankId", items=list(RANK_ITEMS.keys()), default_value=list(RANK_ITEMS.keys())[0], width=100)
                        dpg.add_combo(tag="divisionId", items=list(DIVISION_ITEMS.keys()), default_value=list(DIVISION_ITEMS.keys())[0], width=50)
                        dpg.add_combo(tag="queueId", items=list(QUEUE_ITEMS.keys()), default_value=list(QUEUE_ITEMS.keys())[0], width=165)
                        dpg.add_button(label="Import", callback=lambda:sightstone_hook.set_rank(
                            rank=RANK_ITEMS[dpg.get_value("rankId")],
                            division=DIVISION_ITEMS[dpg.get_value("divisionId")],
                            queue=QUEUE_ITEMS[dpg.get_value("queueId")]
                        ))
                        dpg.add_button(label="Empty", callback=lambda:sightstone_hook.set_rank(
                            rank="",
                            division="",
                            queue="",
                        ))
                dpg.add_separator()
                
                with dpg.group():
                    dpg.add_text("Challenges:")
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
                dpg.add_button(label="Reveal Lobby",
                                callback=lambda:sightstone_hook.open_website(
                                     website=dpg.get_value("revealWebsite"),
                                     multi=True,
                                     query=sightstone_hook.transform_participants_into_query(set(["lipe#69420", "MISSING KERIA ON#000", "naive#444", "wolfs child#EUW"]))))
                dpg.add_button(label="get group",
                               callback=sightstone_hook.get_groups)

                dpg.add_button(label="QUEUE", callback=sightstone_hook.get_queues)
                dpg.add_button(label="muselfg", callback=lambda:sightstone_hook.search_myself(SC.OP_GG))
    dpg.set_primary_window("p1", True)

    # safe title for riot detection sake
    letter_dict = string.ascii_letters + string.digits + string.punctuation
    safe_title = "".join(random.choice(letter_dict) for _ in range(20))
    dpg.create_viewport(
        title=safe_title,
        width=WIDTH, height=HEIGHT,
        resizable=False,
        small_icon="data/icon.ico", large_icon="data/icon.ico"
    )
    dpg.show_viewport()

    # Start threading
    start_threads(sightstone_hook)

    dpg.setup_dearpygui()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()

def start_threads(sightstone_hook: Sightstone):
    """Starts threading"""
    global update_friend_groups_thread
    update_friend_groups_thread = BackgroundThread(
        fn_to_run=lambda:update_friend_groups(sightstone_hook),
        time_between_runs=UPDATE_FRIEND_GROUPS_TIMEOUT,
        daemon=True,
        description="UpdateFriendGroupThread"
    )
    update_friend_groups_thread.start()

    global update_info_label_thread
    update_info_label_thread = BackgroundThread(
        fn_to_run=lambda:update_info_label(sightstone_hook),
        time_between_runs=UPDATE_INFO_LABEL_TIMEOUT,
        daemon=True,
        description="UpdateInfoLabelThread"
    )
    update_info_label_thread.start()


# Module that handles gui

import string
import random
from threading import Thread
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

"""Champ skins"""
global champ_skins
champ_skins: dict[str, dict]

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

update_champ_skins_thread: Thread
def update_champ_skins(sightstone_hook: Sightstone):
    """Update champ skins varaiable for skin & champion storing"""
    global champ_skins
    champ_skins = sightstone_hook.get_champion_skins()

    # Sort
    champ_skins = dict(sorted(champ_skins.items()))

    # Update background collapse with info
    for champ in champ_skins:
        with dpg.tree_node(parent="backgroundCollapse", label=champ):
            for skin in champ_skins[champ]["skins"]:
                # How is this lambda working? I have no idea.
                # it is probably something dumb with python JIT memory,
                # if we dont set the button tag to skin[0], we get the wrong number on set_background(),
                # even though we do not ever touch the button's tag.
                # But if we "refresh" the memory with tag=skin[0] we get the right id to search.
                # Any setting like _skin[0] will set `s` to that.
                # DO NOT TOUCH THIS =P.
                dpg.add_button(label=skin, tag=skin[0], callback=lambda s=skin: sightstone_hook.set_background(s))
                

# pylint: disable=R0915
def init_gui(sightstone_hook: Sightstone):
    """Inits dearpygui window"""
    dpg.create_context()

    # Create champ skins thread firstly
    global update_champ_skins_thread 
    update_champ_skins_thread = Thread(target=lambda:update_champ_skins(sightstone_hook), daemon=True)
    update_champ_skins_thread.start()

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
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Remove Challenges", callback=lambda:sightstone_hook.set_challenges([]))
                        dpg.add_button(label="Copy 1st to all 3", callback=sightstone_hook.copy_first_to_all_challenges)
                    with dpg.group(horizontal=True):
                        dpg.add_text("Glitched:")
                        dpg.add_button(label="0", callback=lambda:sightstone_hook.set_challenges([0, 0, 0]))
                        dpg.add_button(label="1", callback=lambda:sightstone_hook.set_challenges([1, 1, 1]))
                        dpg.add_button(label="2", callback=lambda:sightstone_hook.set_challenges([2, 2, 2]))
                        dpg.add_button(label="3", callback=lambda:sightstone_hook.set_challenges([3, 3, 3]))
                        dpg.add_button(label="4", callback=lambda:sightstone_hook.set_challenges([4, 4, 4]))
                        dpg.add_button(label="5", callback=lambda:sightstone_hook.set_challenges([5, 5, 5]))
                dpg.add_separator()

                with dpg.group():
                    dpg.add_text("Mastery Points:")
                    with dpg.group(horizontal=True):
                        dpg.add_input_int(tag="masteryInput", width=400, min_value=1, min_clamped=True, default_value=1)
                        dpg.add_button(label="Submit", callback=lambda:sightstone_hook.set_mastery_points(dpg.get_value("masteryInput")))
                        dpg.add_button(label="Max", callback=lambda:sightstone_hook.set_mastery_points(-1))
                        dpg.add_button(label="None", callback=lambda:sightstone_hook.set_mastery_points(0))
                dpg.add_separator()

                with dpg.group():
                    dpg.add_text("Icon:")
                    with dpg.group(horizontal=True):
                        dpg.add_input_int(tag="iconInput", width=125, min_value=0, min_clamped=True)
                        dpg.add_button(label="Submit", callback=lambda:sightstone_hook.set_icon(dpg.get_value("iconInput")))
                        dpg.add_button(label="Glitched", callback=lambda:sightstone_hook.set_icon("31"))
                dpg.add_separator()

                with dpg.collapsing_header(label="Backgrounds", tag="backgroundCollapse"):
                    # This will be created at runtime by a champ skins thread
                    pass

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
                dpg.add_button(label="Get champ skins", callback=sightstone_hook.get_champion_skins)
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


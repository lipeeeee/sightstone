# Sightstone constants

SIGHTSTONE = "Sightstone"

# Lobby creation
CLASH_ID            = "700"
QUICK_PLAY_ID       = "490"
ARAM_PLAY_ID        = "450"
DRAFT_PICK_ID       = "400"
FLEX_PLAY_ID        = "440"
SOLO_DUO_ID         = "420"
ARURF_ID            = "900"
ARURF_1V1_ID        = "901"
NEXUS_BLITZ_ID      = "1300"
TFT_NORMAL_ID       = "2200"
TFT_RANKED_ID       = "1100"
TFT_TUTORIAL_ID     = "1110"
TFT_DOUBLE_UP_ID    = "1160"
TFT_HYPERROLL_ID    = "1130"
PRACT_TOOL_JSON     = {
    "customGameLobby":{
        "configuration":
            {
                "gameMode":"PRACTICETOOL",
                "gameMutator":"",
                "gameServerRegion":"",
                "mapId":11,
                "mutators":{"id":1},
                "spectatorPolicy":"AllAllowed",
                "teamSize":1
            },
            "lobbyName":SIGHTSTONE,
            "lobbyPassword":None
    },
    "isCustom":True
}
PRACT_TOOL_5V5_JSON = {
    "customGameLobby":{
        "configuration":
            {
                "gameMode":"PRACTICETOOL",
                "gameMutator":"",
                "gameServerRegion":"",
                "mapId":11,
                "mutators":{"id":1},
                "spectatorPolicy":"AllAllowed",
                "teamSize":5
            },
            "lobbyName":SIGHTSTONE,
            "lobbyPassword":None
    },
    "isCustom":True
} 

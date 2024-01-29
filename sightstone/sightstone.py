# Main cheat engine

import requests
from lca_hook import LeagueConnection
import sightstone_constants as SC

class Sightstone:
    """Sightstone engine for league QOL hacking"""

    lca_hook: LeagueConnection

    def __init__(self) -> None:
        self.lca_hook = LeagueConnection()

    def remove_challenges(self) -> bool:
        """Remove League Challenges

        Remove League of Legends challenges from profile
        using RIOT's auth to LCA
        """
        response = self.lca_hook.post(
            path="lol-challenges/v1/update-player-preferences/",
            json={"challengeIds": []},
        )

        return self.is_valid_response(response)

    def get_queues(self) -> bool:
        """Get all queues present in LCA"""
        response = self.lca_hook.get(
            path="lol-game-queues/v1/queues/"
        )
        if response:
            print(response.json())
        return self.is_valid_response(response)

    def create_lobby(self, lobby_id: str, custom: dict | None = None) -> bool:
        """Creates lobby given an ID"""
        response = self.lca_hook.post(
            path="lol-lobby/v2/lobby/",
            json={"queueId": lobby_id} if not custom else custom,
        )

        return self.is_valid_response(response)

    def set_positions(self, pos1: str, pos2: str) -> bool:
        """Sets positions in lobby"""
        response = self.lca_hook.put(
            path="lol-lobby/v1/lobby/members/localMember/position-preferences/",
            json={"firstPreference": pos1, "secondPreference": pos2}
        )

        return self.is_valid_response(response)

    def custom_game_json(self, game_mode: str, team_size: int, map_code: int) -> dict:
        """Returns the json for a custom game, given `gamemode`, `teamsize` and `map`"""
        return {
           "customGameLobby":{
                "configuration":
                    {
                        "gameMode":game_mode,
                        "gameMutator":"",
                        "gameServerRegion":"",
                        "mapId":map_code,
                        "mutators":{"id":1},
                        "spectatorPolicy":"AllAllowed",
                        "teamSize":team_size
                    },
                    "lobbyName":SC.SIGHTSTONE,
                    "lobbyPassword":None
            },
            "isCustom":True
        }

    def get_current_patch(self):
        """Get current patch"""
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        return response.json()[0]

    def get_current_user(self):
        """Get current client user"""
        response = self.lca_hook.get(
            path="lol-summoner/v1/current-summoner/",
        )

        if response and self.is_valid_response(response):
            return response.json()["gameName"] + "#" + response.json()["tagLine"]

        return None

    def create_lobby_with_positions(self, lobby_id: str, pos1: str, pos2: str) -> bool:
        """Creates league lobby with set positions"""
        return self.create_lobby(lobby_id) and self.set_positions(pos1, pos2)

    def is_valid_response(self, response: requests.Response | None):
        """Checks if the response is valid"""
        return not (response is None or response.status_code in (204, 500))

    def __str__(self) -> str:
        return "instance<class Sightstone>"

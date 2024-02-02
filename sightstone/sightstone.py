# Main cheat engine

import requests
import webbrowser
from lca_hook import LeagueConnection
from lib.background_thread import BackgroundThread
import sightstone_constants as SC

class Sightstone:
    """Sightstone engine for league QOL hacking"""

    QUEUE_FOUND = "Found"
    AUTO_ACCEPT_QUEUE_TIMEOUT = 7

    lca_hook: LeagueConnection
    accept_listener: BackgroundThread # Auto queue accept listener

    def __init__(self) -> None:
        self.lca_hook = LeagueConnection()
        self.accept_listener = BackgroundThread(
            fn_to_run=self.queue_accept, time_between_runs=self.AUTO_ACCEPT_QUEUE_TIMEOUT, daemon=True
        )
        self.__accept_listener_running = False

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

    def dodge_lobby(self) -> bool:
        """Dodges current lobby"""
        lobby_hack = 'destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","quitV2",""]'
        response = self.lca_hook.post(path=f'lol-login/v1/session/invoke?{lobby_hack}')

        return self.is_valid_response(response)

    def start_queue(self) -> bool:
        """Start queue"""
        response = self.lca_hook.post(path="lol-lobby/v2/lobby/matchmaking/search/")

        return self.is_valid_response(response)

    def delete_lobby(self) -> bool:
        """Deletes lobby"""
        response = self.lca_hook.delete(path="lol-lobby/v2/lobby/")
        
        return self.is_valid_response(response)

    def toggle_accept_listener(self):
        """Toggles the auto accept thread"""
        # Start thread if first time
        if not self.accept_listener.started:
            self.accept_listener.start()
            self.__accept_listener_running = True
        # If it is not first time we just toggle
        else:
            self.__accept_listener_running = not self.__accept_listener_running 

    def queue_accept(self):
        """Accept queue if Found"""
        if not self.__accept_listener_running or not self.lca_hook.connected:
            return
        response = self.lca_hook.get(path="lol-lobby/v2/lobby/matchmaking/search-state/")
        if response and response.json()["searchState"] == self.QUEUE_FOUND:
            self.lca_hook.post(path="lol-matchmaking/v1/ready-check/accept/")

    def reveal_lobby(self):
        """Reveal ranked teamates"""
        response = self.lca_hook.riot_get(path="chat/v5/participants")
        if response:
            summNames:list[str] = list()
            for entry in response.json()["participants"]:
                summNames.append(f"{entry['game_name']}#{entry['game_tag']}")
            return set(summNames[-5:]) # Get last 5

    def open_website_on_reveal(self, website, query):
        """Opens lobby checking website with a given query"""
        if not query:
            return
        
        # compile url with query
        url = None
        match website:
            case SC.OP_GG:
                url = f"https://{self.lca_hook.region}.op.gg/multi/query={query}"
            case SC.U_GG:
                query = query.replace("%23", "-")
                url = f"https://u.gg/multisearch?summoners={query}&region={str(self.lca_hook.region).lower()}"

        if url:
            webbrowser.open(url)

    def get_available_bots(self):
        """Gets available bots"""
        response = self.lca_hook.get(path="lol-lobby/v2/lobby/custom/available-bots/")
        if response:
            return response.json()

    def add_bot(self, bot_difficulty: str, team: str, champion_id: str) -> bool:
        """Send request to add bot"""
        response = self.lca_hook.post(
            path="lol-lobby/v1/lobby/custom/bots/",
            json={"botDifficulty": bot_difficulty, "championId": champion_id, "teamId": team},
        )

        return self.is_valid_response(response)

    def get_current_patch(self) -> str:
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

    def transform_participants_into_query(self, participants: set[str] | None):
        """Transforms the return of reveal lobby(list(name#tag)) into a URL readable format"""
        if not participants:
            return None

        query: str = ""
        for participant in participants:
            query += participant.replace("#", "%23") + ","
        return query[:-1]

    def create_lobby_with_positions(self, lobby_id: str, pos1: str, pos2: str) -> bool:
        """Creates league lobby with set positions"""
        return self.create_lobby(lobby_id) and self.set_positions(pos1, pos2)

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

    def is_valid_response(self, response: requests.Response | None):
        """Checks if the response is valid"""
        return not (response is None or response.status_code in (204, 500))

    def __str__(self) -> str:
        return "instance<class Sightstone>"

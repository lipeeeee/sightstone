# Main cheat engine

from typing import Any
import requests
import webbrowser
import subprocess
from sightstone.lca_hook import LeagueConnection
from sightstone.background_thread import BackgroundThread
import sightstone.sightstone_constants as SC

class Sightstone:
    """Sightstone engine for league QOL hacking
   
    Sightstone is a Multipurpose league __CLIENT__ hack to give the user much more acess 
    than riot orignally intended, from dodging lobbies without leaving the game to being able to
    completely control your profile and doing actions the client does not normally allow us, like removing challenges
    or seeing what are your teamates in ranked.
    """

    AUTO_ACCEPT_QUEUE_TIMEOUT = 7
    AVAILABLE_WEBSITES = [ SC.OP_GG ] # All supported websites for data display

    URI_HASHTAG = "%23" # Represents url readable hashtag
    URI_SPACE   = "%20" # Represents url readable space

    lca_hook: LeagueConnection
    accept_listener: BackgroundThread # Auto queue accept listener

    def __init__(self) -> None:
        self.lca_hook = LeagueConnection()
        self.accept_listener = BackgroundThread(
            fn_to_run=self.queue_accept, time_between_runs=self.AUTO_ACCEPT_QUEUE_TIMEOUT,
            daemon=True, description="sightstone.accept_listener"
        )
        self.__accept_listener_running = False

    def get_queues(self) -> list[dict]:
        """Get all queues present in LCA"""
        response = self.lca_hook.get(path="lol-game-queues/v1/queues/")
        
        if response:
            return response.json()
        return list()

    def get_friends(self) -> dict:
        """Get friends"""
        response = self.lca_hook.get(path="lol-chat/v1/friends")

        if response:
            return response.json()
        return dict()
    
    def get_groups(self) -> list[dict]:
        """Get's all friend's group"""
        response = self.lca_hook.get(path="lol-chat/v1/friend-groups/")
        
        if response:
            return response.json()
        else:
            return list()

    def get_champion_skins(self) -> tuple[dict[str, dict], dict[str, str]]:
        """Get champion & their skins
        
        returned structure:
            dict1[champName][id] = json_id
            dict1[champName][key] = json_id / 100 
            dict1[champName][skins] = list(tuple(id, name))
            dict2[id] = name
        """
        response = requests.get("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json")
        json = response.json()
        current_champ_name = str()
        champ_skins: dict[str, dict] = dict()
        skins_name_by_id: dict[str, str] = dict()

        for id in json:
            element = json[id]
            skins_name_by_id[id] = element["name"]
            if element["isBase"] == True:
                current_champ_name = element["name"]
                champ_skins[current_champ_name] = dict()
                champ_skins[current_champ_name]["id"] = id
                champ_skins[current_champ_name]["key"] = int(id) // 100
                champ_skins[current_champ_name]["skins"] = list()
                champ_skins[current_champ_name]["skins"].append((id, "Default"))
            else:
                champ_skins[current_champ_name]["skins"].append((id, element["name"]))

        return (champ_skins, skins_name_by_id)

    def get_current_patch(self) -> str:
        """Get current patch from external source"""
        # If this request fails, something has gone very wrong
        try:
            response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
            return response.json()[0]
        except:
            return str()

    def get_loot(self) -> dict:
        """Get's player loot"""
        response = self.lca_hook.get(
            path="lol-loot/v1/player-loot-map/"
        )

        if response:
            return response.json()
        return dict()

    def get_current_user(self) -> str | None:
        """Get current client user"""
        response = self.lca_hook.get(path="lol-summoner/v1/current-summoner/")

        if response and self.is_valid_response(response):
            return response.json()["gameName"] + "#" + response.json()["tagLine"]
        return None

    def get_all_friend_requests(self) -> dict:
        """Get's all friend requests"""
        response = self.lca_hook.get(path="lol-chat/v1/friend-requests")

        if response:
            return response.json()
        return dict()

    def get_player_skins(self) -> dict:
        """Get player champion skins"""
        response = self.lca_hook.get(path="lol-inventory/v2/inventory/CHAMPION_SKIN/")

        if response:
            return response.json()
        return dict()

    def get_current_session(self) -> dict:
        """Get current session data"""
        response = self.lca_hook.get(path="lol-login/v1/session/")

        if response:
            return response.json()
        return dict()

    def get_player_info(self, name: str) -> dict:
        """Gets player info, given a name"""
        response = self.lca_hook.get(
            path=f"lol-summoner/v1/summoners?name={name.replace('#', self.URI_HASHTAG)}"
        )
        
        if response != None:
            return response.json()
        return dict()

    def count_champions_owned(self, optional_champ_dict: dict | None = None) -> int:
        """Count champions owned"""
        champ_dict: dict
        if optional_champ_dict:
            champ_dict = optional_champ_dict
        else:
            champ_dict = self.get_champion_data(self.get_current_session()["summonerId"])

        if not champ_dict or len(champ_dict) == 0:
            return -1
        
        count = 0
        for champ in champ_dict:
            if bool(champ["ownership"]["owned"]):
                count += 1
        return count

    def get_champion_data(self, summoner_id: str) -> dict:
        """Get minimal champion data"""
        response = self.lca_hook.get(
            path=f"lol-champions/v1/inventories/{summoner_id}/champions-minimal/"
        )

        if response:
            return response.json()
        return dict()

    def get_champion_mastery(self, summoner_id: str) -> dict:
        """Get champion mastery data"""
        response = self.lca_hook.get(
            path=f"lol-collections/v1/inventories/{summoner_id}/champion-mastery/"
        )

        if response:
            return response.json()
        return dict()

    def start_queue(self) -> bool:
        """Start queue"""
        response = self.lca_hook.post(path="lol-lobby/v2/lobby/matchmaking/search/")

        return self.is_valid_response(response)

    def delete_lobby(self) -> bool:
        """Deletes lobby"""
        response = self.lca_hook.delete(path="lol-lobby/v2/lobby/")
        
        return self.is_valid_response(response)

    def dodge_lobby(self) -> bool:
        """Dodges current lobby"""
        lobby_hack = 'destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","quitV2",""]'
        response = self.lca_hook.post(path=f'lol-login/v1/session/invoke?{lobby_hack}')

        return self.is_valid_response(response)

    def disenchant_all(self, group: str) -> int:
        """Disenchant all loot from a given group"""
        all_loot = self.get_loot()
        disenchanted = 0

        for loot in all_loot:
            if group == all_loot[loot]["type"]:
                self.disenchant_loot(group, loot)
                disenchanted += 1
        return disenchanted

    def disenchant_loot(self, disenchant_type: str, disenchant_name: str) -> bool:
        """Disenchant loot given name"""
        disenchant_string = 'DISENCHANT' if disenchant_type in [SC.ETERNAL_TYPE_1, SC.ETERNAL_TYPE_2] else 'disenchant'
        response = self.lca_hook.post(
            path=f"lol-loot/v1/recipes/{disenchant_type}_{disenchant_string}/craft?repeat=1",
            json=[disenchant_name])
        return self.is_valid_response(response)

    def invite_to_lobby(self, summoner_id: str) -> bool:
        """Invite to lobby a summoner id"""
        # Have to use a custom POST request because this endpoint only accepts vectors
        response = self.lca_hook.post(
            path="lol-lobby/v2/lobby/invitations/",
            json=[{"toSummonerId": summoner_id}])

        return self.is_valid_response(response)

    def send_friend_invite(self, game_name: str, tag_line: str) -> bool:
        """Send riot friend invite"""
        response = self.lca_hook.post(
            path="lol-chat/v2/friend-requests/",
            json={"gameName": game_name, "tagLine": tag_line}
        )

        return self.is_valid_response(response)

    def accept_friend_request(self, request_id: str) -> bool:
        """Accept's friend request"""
        response = self.lca_hook.put(
            path=f"lol-chat/v1/friend-requests/{request_id}",
            json={"direction": "both"}
        )

        return self.is_valid_response(response)

    def reject_friend_request(self, request_id: str) -> bool:
        """Reject's friend request"""
        response = self.lca_hook.delete(
            path=f"lol-chat/v1/friend-requests/{request_id}",
        )

        return self.is_valid_response(response)

    def accept_all_friend_requests(self) -> int:
        """Accept's all friend requests"""
        all_requests: dict = self.get_all_friend_requests()
        print(all_requests)
        
        for request in all_requests:
            self.accept_friend_request(request["pid"])
        return len(all_requests)

    def reject_all_friend_request(self) -> int:
        """Reject's all friend requests"""
        all_requests: dict = self.get_all_friend_requests()
        
        for request in all_requests:
            self.reject_friend_request(request["pid"])
        return len(all_requests)

    def block_player(self, summoner_id: str) -> bool:
        """Block player"""
        response = self.lca_hook.post(
            path="lol-chat/v1/blocked-players/",
            json={"summonerId": summoner_id}
        )

        return self.is_valid_response(response)

    def invite_friends_from_group(self, group: str) -> None:
        """Invite all friends from specific group"""
        friends = self.get_friends()
        if len(friends) == 0:
            return

        for friend in friends:
            if friend["groupName"] == group:
                self.invite_to_lobby(friend["summonerId"])

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
        if response and response.json()["searchState"] == SC.QUEUE_FOUND:
            self.lca_hook.post(path="lol-matchmaking/v1/ready-check/accept/")

    def get_available_bots(self) -> list[dict]:
        """Gets available bots"""
        response = self.lca_hook.get(path="lol-lobby/v2/lobby/custom/available-bots/")
        if response:
            return response.json()
        return list()

    def add_bot(self, bot_difficulty: str, team: str, champion_id: str) -> bool:
        """Send request to add bot"""
        response = self.lca_hook.post(
            path="lol-lobby/v1/lobby/custom/bots/",
            json={"botDifficulty": bot_difficulty, "teamId": team, "championId": champion_id},
        )

        return self.is_valid_response(response)

    def create_lobby(self, lobby_id: str, custom: dict | None = None) -> bool:
        """Creates lobby given an ID"""
        response = self.lca_hook.post(
            path="lol-lobby/v2/lobby/",
            json={"queueId": lobby_id} if not custom else custom,
        )

        return self.is_valid_response(response)

    def remove_friend(self, summoner_id: str) -> bool:
        """Remove friend"""
        response = self.lca_hook.delete(
            path=f"lol-chat/v1/friends/{summoner_id}"
        )

        return self.is_valid_response(response)

    def remove_friend_from_group(self, group: str) -> int:
        """Remove friend's from group"""
        friends = self.get_friends()

        for friend in friends:
            if friend["groupName"] == group:
                self.remove_friend(friend["pid"])
        return len(friends)

    def restart_client_ux(self) -> bool:
        """Restarts client UX"""
        response = self.lca_hook.post(
            path="riotclient/kill-and-restart-ux/"
        )

        return self.is_valid_response(response)

    def launch_client(self) -> None:
        """Launch's another client"""
        subprocess.run([self.lca_hook.complete_league_path, "--allow-multiple-clients"])

    def close_client(self) -> bool:
        """Close client"""
        response = self.lca_hook.post(
            path="process-control/v1/process/quit/"
        )
        
        return self.is_valid_response(response)

    def set_rank(self, rank: str, division: str, queue: str) -> bool:
        """Set client rank(on hover)"""
        response = self.lca_hook.put(
            path="lol-chat/v1/me/",
            json={"lol": {"rankedLeagueQueue": queue, "rankedLeagueTier": rank, "rankedLeagueDivision": division}}
        )

        return self.is_valid_response(response)

    def set_mastery_points(self, mastery_points: int) -> bool:
        """Set profile mastery points"""
        response = self.lca_hook.put(
            path="lol-chat/v1/me/",
            json={"lol": {"masteryScore": str(mastery_points)}}
        )

        return self.is_valid_response(response)

    def set_background(self, background_id: int) -> bool:
        """Set's profile background splashart"""
        response = self.lca_hook.post(
            path="lol-summoner/v1/current-summoner/summoner-profile/",
            json={"key":"backgroundSkinId", "value": background_id}
        )

        return self.is_valid_response(response)

    def set_icon(self, icon_id: str) -> bool:
        """Set icon"""
        response = self.lca_hook.put(
            path="lol-summoner/v1/current-summoner/icon/",
            json={"profileIconId": icon_id}
        )

        return self.is_valid_response(response)

    def set_positions(self, pos1: str, pos2: str) -> bool:
        """Sets positions in lobby"""
        response = self.lca_hook.put(
            path="lol-lobby/v1/lobby/members/localMember/position-preferences/",
            json={"firstPreference": pos1, "secondPreference": pos2}
        )

        return self.is_valid_response(response)

    def create_lobby_with_positions(self, lobby_id: str, pos1: str, pos2: str) -> bool:
        """Creates league lobby with set positions"""
        return self.create_lobby(lobby_id) and self.set_positions(pos1, pos2)

    def open_website(self, website: str | None, query: str | None, multi: bool = False) -> None:
        """Open's data checking website(op.gg, u.gg, etc...) with a given query"""
        if not query or not website:
            return
        
        # Compile url given the website & multi
        url = None
        match website:
            case SC.OP_GG:
                if multi:
                    url = f"https://{self.lca_hook.region}.op.gg/multi/query={query}"
                else:
                    url = f"https://op.gg/summoners/{self.lca_hook.region}/{query.replace(self.URI_HASHTAG, '-')}"
        
        # Open if could parse
        if url:
            webbrowser.open(url)

    def search_lobby(self, website: str | None) -> None:
        """Searches current lobby in a website"""
        if not website:
            return

        # Get participants
        participants = self.reveal_lobby()
        if len(participants) == 0:
            return
        
        # Compile query
        query = self.transform_participants_into_query(participants)
        
        # Open website
        self.open_website(website=website, query=query, multi=True)

    def reveal_lobby(self) -> set[str]:
        """Reveal ranked teamates, This uses special riot acess"""
        response = self.lca_hook.riot_get(path="chat/v5/participants/")
        if response:
            summNames:list[str] = list()
            for entry in response.json()["participants"]:
                summNames.append(f"{entry['game_name']}#{entry['game_tag']}")
            return set(summNames[-5:]) # Get last 5
        return set()
    
    def transform_participants_into_query(self, participants: set[str] | None) -> str | None:
        """Transforms the return of reveal lobby(list(name#tag)) into a URL readable format"""
        if not participants:
            return None

        query: str = ""
        for participant in participants:
            query += participant.replace("#", self.URI_HASHTAG) + ","
        return query[:-1] # Without last ","

    def search_myself(self, website: str) -> None:
        """Opens connected player's data website"""
        user = self.get_current_user()
        if user:
            self.open_website(website=website, query=user.replace("#", self.URI_HASHTAG))

    def import_status_txt(self, text: str) -> bool:
        """Import text part of status"""
        response = self.lca_hook.put(
            path="lol-chat/v1/me/",
            json={"statusMessage": text}
        )

        return self.is_valid_response(response)

    def import_status_availability(self, availability: str) -> bool:
        """Imports availability part of status"""
        response = self.lca_hook.put(
            path="lol-chat/v1/me",
            json={"availability": availability}
        )

        return self.is_valid_response(response)
    
    def import_status(self, text: str, availability: str) -> bool:
        """Imports both status text and availability"""
        return self.import_status_txt(text) and self.import_status_availability(availability)

    def set_challenges(self, challenges: list) -> bool:
        """Set challenges"""
        self.get_player_preferences()
        response = self.lca_hook.post(
            path="lol-challenges/v1/update-player-preferences/",
            json={"challengeIds": challenges}
        )
        return self.is_valid_response(response)

    def copy_first_to_all_challenges(self) -> bool:
        """Copies first challenge to all 3"""
        preferences = self.get_player_preferences()
        if len(preferences) == 0:
            return False
   
        # If IndexError it means that there is not first challenge
        try:
            first_challenge = preferences["topChallenges"][0]["id"] 
            return self.set_challenges([first_challenge, first_challenge, first_challenge])
        except IndexError:
            return False

    def get_player_preferences(self) -> dict:
        """Gets player preferences"""
        response = self.lca_hook.get(
            path="lol-challenges/v1/summary-player-data/local-player/",
        )
        if response:
            return response.json()
        return dict()

    def submit_ingame_settings(self, settings: Any) -> bool:
        """Submit ingame settings"""
        response = self.lca_hook.patch(
            path="lol-game-settings/v1/game-settings/",
            json=settings
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

    def is_valid_response(self, response: requests.Response | None) -> bool:
        """Checks if the response is valid"""
        return not (response is None or response.status_code in (204, 400, 401, 402, 500))

    def __str__(self) -> str:
        all_callable_funcs = [x for x in dir(self) if callable(getattr(self, x)) and not x.startswith("__")]
        return f"instance<class Sightstone>:{all_callable_funcs}"

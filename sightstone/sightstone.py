# Main cheat engine

from requests import Response
from lca_hook import LeagueConnection

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
        """."""
        response = self.lca_hook.get(
            path="lol-game-queues/v1/queues/"
        )
        if response:
            print(response.json())
            exit(1)
        return self.is_valid_response(response)
    
    def create_lobby(self, id: str) -> bool:
        """Creates lobby given an ID"""
        response = self.lca_hook.post(
            path="lol-lobby/v2/lobby",
            json={"queueId": id},
        )
        if response:
            print(response.json())
        return self.is_valid_response(response)

    def is_valid_response(self, response: Response | None):
        """Checks if the response is valid"""
        return not (response is None or response.status_code in (204, 500))

    def __str__(self) -> str:
        return "instance<class Sightstone>"

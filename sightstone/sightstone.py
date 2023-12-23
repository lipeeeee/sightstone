# Main cheat engine

import sys
sys.path.append("./sightstone")
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
       
        return not (response is None or response.status_code != 204)

    def __str__(self) -> str:
        return "instance<class Sightstone>"

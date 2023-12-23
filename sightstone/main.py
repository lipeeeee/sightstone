# Sightstone entry point

from gui import init_gui
from sightstone import Sightstone
from league_api_hook import LeagueConnection

def main():
    init_gui("")

if __name__ == "__main__":
    main()

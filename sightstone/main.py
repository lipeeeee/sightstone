# Sightstone entry point

from gui import init_gui
from sightstone import Sightstone
from lca_hook import LeagueConnection

def main():
    sightstone_engine = Sightstone()
    init_gui(sightstone_engine)

if __name__ == "__main__":
    main()

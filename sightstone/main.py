# Sightstone entry point

from sightstone.gui import init_gui
from sightstone.sightstone import Sightstone

def main():
    sightstone_engine = Sightstone()
    init_gui(sightstone_engine)

if __name__ == "__main__":
    main()

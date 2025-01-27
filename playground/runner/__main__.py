from apexdevkit.server import UvicornServer

from playground.runner.setup import MemoryType, setup

if __name__ == "__main__":
    UvicornServer.from_env().run(setup(MemoryType.SQL_LITE))

import sc2
from sc2 import run_game, maps, Race
from sc2.player import Bot, Human

map_dir = "C:\\Users\CODE\Desktop\Ladder2018Season2\\16-BitLE"


class WorkerRushBot(sc2.BotAI):
    # on_step function is called for every game step
    # it takes current game state and iteration
    async def on_step(self, iteration):
        # if it is the first frame on the game
        # if iteration == 0:
        #     for worker in self.workers:
        #         # have the worker attack the enemy start position
        #         await self.do(worker.attack(self.enemy_start_locations[0]))

        if self.supply_left <= 5:
            self.select_build_worker(self.townhalls.center, force=True)


run_game(maps.get(map_dir), [
    Human(Race.Protoss),
    Bot(Race.Random, WorkerRushBot())
], realtime=True)

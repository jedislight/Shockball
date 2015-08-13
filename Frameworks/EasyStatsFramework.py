import Simulation
import Frameworks.PlayerStatsPrebuilts as PlayerStatsPrebuilts

class EasyStatsFramework(Simulation.AI):
    def __init__(self):
        self.stats = [PlayerStatsPrebuilts.balanced, PlayerStatsPrebuilts.balanced, PlayerStatsPrebuilts.balanced]
        
    def GetPlayerStats(self, player_number):
        return self.stats[player_number - 1]
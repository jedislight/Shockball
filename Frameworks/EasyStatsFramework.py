'''
An easier way to setup stats, simply set self.stats to an array of 3 PlayerStats objects for your players, no need to define GetPlayerStats yourself
'''
from AI import AI
import Frameworks.PlayerStatsPrebuilts as PlayerStatsPrebuilts

class EasyStatsFramework(AI):
    def __init__(self):
        self.stats = [PlayerStatsPrebuilts.balanced, PlayerStatsPrebuilts.balanced, PlayerStatsPrebuilts.balanced]
        
    def GetPlayerStats(self, player_number):
        return self.stats[player_number - 1]
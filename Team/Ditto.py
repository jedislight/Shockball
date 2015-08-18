'''
not sure if bug ... or brillant
'''
from AI import AI

@AI.Team
class Ditto(AI):
    def __init__(self):
        self.other = [team for team in AI.team if team != Ditto][0]()
    
    def Update(self, ai_input):
        return self.other.Update(ai_input)
    
    def GetPlayerStats(self, player_number):
        return self.other.GetPlayerStats(player_number)
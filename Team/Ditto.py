'''
not sure if bug ... or brillant
'''
from AI import AI

@AI.Team
class Ditto(AI):
    def __init__(self):
        try:
            self.other = [team for team in AI.team if team != self.__class__][0]()
        except:
            self.other = None
    
    def Update(self, ai_input):
        if self.other:
            return self.other.Update(ai_input)
        return AI.Update(self, ai_input)
    
    def GetPlayerStats(self, player_number):
        if self.other:
            return self.other.GetPlayerStats(player_number)
        return AI.GetPlayerStats(self, player_number)
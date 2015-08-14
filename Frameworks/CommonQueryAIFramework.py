'''
Common Query Operations, feel like writing GetClosestAttackableOpponent for the 1001th time - I thought not
'''
import math
import vector
from AI import AI

class CommonQueryAIFramework(AI):
    def __init__(self):
        pass
    
    def GetClosestObject(self, origin, objects):
        result = None
        if objects:    
            distances = [(origin - obj.position).length for obj in objects]
            result = objects[distances.index(min(distances))]                    
        return result    
    
    def GetClosest(self, origin, positions):
        result = None
        if positions:    
            distances = [(origin - position).length for position in positions]
            result = positions[distances.index(min(distances))]                    
        return result    
    
    def GetClosestAttackableOpponent(self, player, ai_input):
        target = self.GetClosestObject(player.position, [target for target in ai_input.player_infos if target.team != player.team and target.has_been_hit != True])
        return target
    
    def GetClosestInFlightThrownBall(self, player, ai_input):
        avoid = self.GetClosestObject(player.position, [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw])
        return avoid    
    
    def GetClosestTeamateWithoutBall(self, player, ai_input):
        return self.GetClosestObject(player.position, [player for player in ai_input.player_infos if player.team == ai_input.team and player.has_ball == False])
    
    def GetPlayerNumbered(self, number, ai_input):
        for player in ai_input.player_infos:
            if player.number == number:
                return player
        return None
    
    def GetHitTeammates(self, ai_input):
        return [player for player in ai_input.player_infos if player.team == ai_input.team and player.has_been_hit]
    
    def Distance(self, a, b):
        if type(a) == vector.Vector:
            return (a-b).length
        return (a.position - b.position).length
    
"""
RoadMap:
Prevent friendly fire
"""
import Simulation
import vector

class KaliAI1(Simulation.AI):
    def __init__(self):
        pass
    def Update(self, ai_input):
        output = Simulation.AIOutput()
        #Build Player Update Instructions per Player We Have
        for player in ai_input.player_infos:
            if player.team != ai_input.team:
                continue
            ins = Simulation.PlayerUpdateInstructions(player.number)
            targetable_players = self.GetTargetablePlayers(ai_input, player)
            targeted_player = self.GetClosestOfPositionalObjects(player, targetable_players)
            #First Round Instructions
            #Get Closest Ball
            if not player.has_ball:
                closest_ball = self.GetClosestOfPositionalObjects(player, ai_input.grounded_ball_infos + [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw == False])
                if closest_ball == None:
                    continue #GivePlayerSomethingToDoIfNoBallsAvailable
                if (closest_ball.position - player.position).length < 2:
                    ins.is_picking = True
                else:
                    ins.is_moving = True
                    ins.move_target = closest_ball.position
            #Get Ball to Target Player
            elif targeted_player != None:
                throwing_distance = player.throw * 10
                if (targeted_player.position - player.position).length > throwing_distance:
                    ins.is_moving = True
                    ins.move_target = targeted_player.position
                elif targeted_player.team == player.team:
                    ins.is_passing = True
                    ins.pass_target = targeted_player.position
                else:
                    ins.is_throwing = True
                    ins.throw_target = targeted_player.position
            
            output.player_update_instructions.append(ins)
        return output
    
    def GetTargetablePlayers(self, ai_input, player):
        targetable_players = list()
        for considered_player in ai_input.player_infos:
            if considered_player.has_ball and considered_player.team == player.team:
                continue
            if considered_player.team != player.team:
                targetable_players.append(considered_player)
                continue
            opponent_players = list()
            for opponent in ai_input.player_infos:
                if opponent.team != player.team:
                    opponent_players.append(opponent)
            closest_opponent = self.GetClosestOfPositionalObjects(player, opponent_players)
            if closest_opponent == None:
                continue
            distance = (considered_player.position - closest_opponent.position).length
            max_throwing_distance = considered_player.throw * 10
            if distance <= max_throwing_distance:
                targetable_players.append(considered_player)
        return targetable_players
    
    def GetClosestOfPositionalObjects(self, positional_object, positional_object_list):
        if len(positional_object_list) == 0:
            return None
        closest_positional_object = positional_object_list[0]
        closest_distance = (positional_object.position - positional_object_list[0].position).length
        for considered_positional_object in positional_object_list:
            distance = (positional_object.position - considered_positional_object.position).length
            if distance < closest_distance:
                closest_distance = distance
                closest_positional_object = considered_positional_object
        return closest_positional_object
        
    
            
"""
RoadMap:
Prevent friendly fire
"""
from AI import AI
from AI import PlayerUpdateInstructions
from AI import AIOutput
import vector
from Frameworks.CommonQueryAIFramework import CommonQueryAIFramework
from Frameworks.ActionAIFramework import ActionAIFramework

@AI.Team
class KaliAI1(CommonQueryAIFramework, ActionAIFramework):
    def __init__(self):
        ActionAIFramework.__init__(self)
        self.strategy = [  self.Action_DodgeGoose,
                           self.Action_GetTheFOutOfTheWay,
                           self.Action_GetClosestBall,
                           self.Action_GetBallToTargetPlayer,
                           ]        
        self.actions[1] = self.strategy
        self.actions[2] = self.strategy
        self.actions[3] = self.strategy        

    def Action_DodgeGoose(self, player, ins, ai_input):
        ball = self.GetClosestInFlightThrownBall(player, ai_input)        
        if ball:
            ball_to_player = (player.position - ball.position)
            ball_to_player.normalize()
            bv = vector.Vector(x=ball.velocity.x, y=ball.velocity.y)
            bv.normalize()
            incoming = ball_to_player * bv
            if incoming > 0.75 and self.Distance(player, ball) < 31:
                ins.move_target = ((player.position - ball.position) + player.position)
                ins.is_moving = True
                return True
        return False
    
    def Action_GetBallToTargetPlayer(self, player, ins, ai_input):
        targetable_players = self.GetTargetablePlayers(ai_input, player)
        targeted_player = self.GetClosestOfPositionalObjects(player, targetable_players)
        if targeted_player != None:
            throwing_distance = player.throw * 10
            if (targeted_player.position - player.position).length > throwing_distance:
                ins.is_moving = True
                ins.move_target = targeted_player.position
                return True
            elif targeted_player.team == player.team:
                ins.is_passing = True
                ins.pass_target = targeted_player.position
                return True
            else:
                ins.is_throwing = True
                ins.throw_target = targeted_player.position
                return True
        return False

    def Action_GetClosestBall(self, player, ins, ai_input):
        if not player.has_ball:
            closest_ball = self.GetClosestOfPositionalObjects(player, ai_input.grounded_ball_infos + [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw == False])
            if closest_ball == None:
                return False # GivePlayerSomethingToDoIfNoBallsAvailable
            if (closest_ball.position - player.position).length < 2:
                ins.is_picking = True
                return True
            else:
                ins.is_moving = True
                ins.move_target = closest_ball.position
                return True
        return False

    def Action_GetTheFOutOfTheWay(self, player, ins, ai_input):
        teammates = self.GetTeammates(ai_input)
        for teammate in teammates:
            if teammate.number == player.number:
                continue
            else:
                if self.Distance(teammate, player) < 1.6 and player.number < teammate.number:
                    ins.is_moving = True 
                    ins.move_target = ((player.position - teammate.position) + player.position) #I Totally Know It Is Equivelant To 2x - y, But Reasons.
                    return True
        return False
    
    def GetTargetablePlayers(self, ai_input, player):
        kill = self.GetClosestAttackableOpponent(player, ai_input)
        if kill:
            kill_dst = self.Distance(player, kill)
            if kill_dst <= player.throw * 10:
                return [kill]
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
            closest_opponent = self.GetClosestOfPositionalObjects(considered_player, opponent_players)
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
        
    
            
from AI import AI
from Frameworks.ActionAIFramework import ActionAIFramework
from Frameworks.EasyStatsFramework import EasyStatsFramework
from Frameworks.CommonQueryAIFramework import CommonQueryAIFramework
import Frameworks.PlayerStatsPrebuilts as PlayerStatsPrebuilts
import vector

@AI.Team
class Assassins(ActionAIFramework, EasyStatsFramework, CommonQueryAIFramework):
    def __init__(self):
        ActionAIFramework.__init__(self)
        EasyStatsFramework.__init__(self)
        CommonQueryAIFramework.__init__(self)
        self.stats = [ PlayerStatsPrebuilts.stealer, PlayerStatsPrebuilts.stealer, PlayerStatsPrebuilts.stealer]        
        logic = [self.Action_AvoidIncomingBall, self.Action_GetClosestBall, self.Action_CullTheWeak ,self.Action_AttackClosestOpponent]
        self.actions[1] = logic
        self.actions[2] = logic
        self.actions[3] = logic
        self.weak = 0
        self.delay = 5
        self.time_since_last_throw = 999
        
    def Update(self, ai_input):
        self.time_since_last_throw += 1
        opponent_numbers_that_have_been_hit = [player.number for player in ai_input.player_infos if player.team != ai_input.team and player.has_been_hit]
        opponent_numbers = [player.number for player in ai_input.player_infos if player.team != ai_input.team]
        if self.weak not in opponent_numbers and opponent_numbers_that_have_been_hit:
            self.weak = opponent_numbers_that_have_been_hit[0]
            
        return ActionAIFramework.Update(self, ai_input)
    
    def Action_AvoidIncomingBall(self, player, instructions, ai_input):
        ball = self.GetClosestInFlightThrownBall(player, ai_input)
        if ball:
            ball_to_player = player.position - ball.position
            distance = ball_to_player.length
            if distance < 40 and self.IsBallGoingToward(ball, player.position):
                instructions.move_target = player.position + ball_to_player
                return True
        return False    
    
    def Action_CullTheWeak(self, player, instructions, ai_input):
        target = self.GetPlayerNumbered(self.weak, ai_input)
        blocker = self.GetClosestObject(player.position, [p for p in ai_input.player_infos if p.number != player.number])
        if blocker and blocker.team == player.team and target:
            #just move
            instructions.move_target = target.position
            return True
        elif player.has_ball and target and target.has_been_hit == False:
            instructions.move_target = target.position
            distance = (target.position - player.position).length
            if distance < 8 * player.throw and self.time_since_last_throw > self.delay:
                instructions.is_throwing = True
                instructions.throw_target = target.position
                ai_input.player_infos.remove(target)
            return True
        return False    
    
    def Action_GetClosestBall(self, player, instructions, ai_input):
        if ai_input.grounded_ball_infos and not player.has_ball:
            ball = self.GetClosestObject(player.position, [ball for ball in ai_input.grounded_ball_infos])
            distance = (ball.position - player.position).length
            if distance < 2.0:
                instructions.is_picking = True
            else:
                instructions.move_target = ball.position
            return True
        return False       
    
    def Action_AttackClosestOpponent(self, player, instructions, ai_input):
        target = self.GetClosestAttackableOpponent(player, ai_input)
        blocker = self.GetClosestObject(player.position, [p for p in ai_input.player_infos if p.number != player.number])
        if blocker and blocker.team == player.team and target:
            #just move
            instructions.move_target = target.position
            return True
        elif player.has_ball and target:
            instructions.move_target = target.position
            distance = (target.position - player.position).length
            if distance < 8 * player.throw:
                instructions.is_throwing = True
                instructions.throw_target = target.position
            return True
        return False    
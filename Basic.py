import Simulation
import Frameworks.ActionAIFramework as ActionAIFramework
import Frameworks.EasyStatsFramework as EasyStatsFramework
import Frameworks.CommonQueryAIFramework as CommonQueryAIFramework
import PlayerStatsPrebuilts
import vector

class Basic(ActionAIFramework.ActionAIFramework, EasyStatsFramework.EasyStatsFramework, CommonQueryAIFramework.CommonQueryAIFramework):
    def __init__(self):
        ActionAIFramework.ActionAIFramework.__init__(self)
        EasyStatsFramework.EasyStatsFramework.__init__(self)
        CommonQueryAIFramework.CommonQueryAIFramework.__init__(self)
        logic = [self.Action_GetClosestBall, self.Action_AttackClosestOpponent]
        self.actions[1] = logic
        self.actions[2] = logic
        self.actions[3] = logic
        
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
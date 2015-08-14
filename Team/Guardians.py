from AI import AI
from Frameworks.ActionAIFramework import ActionAIFramework
from Frameworks.EasyStatsFramework import EasyStatsFramework
from Frameworks.CommonQueryAIFramework import CommonQueryAIFramework
import Frameworks.PlayerStatsPrebuilts as PlayerStatsPrebuilts
import vector

@AI.Team
class Guardians(ActionAIFramework, EasyStatsFramework, CommonQueryAIFramework):
    def __init__(self):
        ActionAIFramework.__init__(self)
        EasyStatsFramework.__init__(self)
        CommonQueryAIFramework.__init__(self)
        self.stats = [PlayerStatsPrebuilts.assistant] * 3
        logic = [self.Action_AvoidIncomingBall, self.Action_GetClosestBall, self.Action_CoverRunBacks, self.Action_AttackClosestOpponent, self.Action_MoveToStart]
        self.actions[1] = logic
        self.actions[2] = logic
        self.actions[3] = logic
        self.player_starting_positions = {}
        
    def Update(self, ai_input):
        self.SetupStartingPositionsOnFirstUpdate(ai_input)
        [ai_input.player_infos.remove(player) for player in ai_input.player_infos[:] if player.team != ai_input.team and abs(player.position.y - self.player_starting_positions[player.number].y) < (ai_input.arena_size * 0.6)]
        return ActionAIFramework.Update(self, ai_input)
        
    def Action_MoveToStart(self, player, instructions, ai_input):
        instructions.move_target = vector.Vector(*self.player_starting_positions[player.number])
        center = ai_input.arena_size *0.5
        offset = center - instructions.move_target.x
        instructions.move_target.x += offset * 0.25
        return True
        
    def Action_CoverRunBacks(self, player, instructions, ai_input):
        if player.has_ball:
            hit_teammates = self.GetHitTeammates(ai_input)
            if hit_teammates:
                ward = hit_teammates[0]
                instructions.move_target = ward.position
                threat = self.GetClosestAttackableOpponent(ward, ai_input)
                if threat:
                    threat_distance = self.Distance(ward, threat)
                    if threat_distance < 40:
                        instructions.move_target = threat.position
                        if threat_distance < player.throw * 6:
                            instructions.is_throwing = True
                            instructions.throw_target = threat.position           
        return False
        
    def Action_AvoidIncomingBall(self, player, instructions, ai_input):
        ball = self.GetClosestInFlightThrownBall(player, ai_input)
        if ball:
            ball_to_player = player.position - ball.position
            distance = ball_to_player.length
            if distance < 40:
                angel_of_approach = ball_to_player * ball.velocity
                if angel_of_approach > .5:
                    instructions.move_target = player.position + ball_to_player
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
            ai_input.grounded_ball_infos.remove(ball)
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
    
    def SetupStartingPositionsOnFirstUpdate(self, ai_input):
        if len(self.player_starting_positions) == 0:    
            for player in ai_input.player_infos:
                self.player_starting_positions[player.number] = player.position
    
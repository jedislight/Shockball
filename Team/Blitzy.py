from AI import AI
from AI import PlayerUpdateInstructions
from Frameworks.ActionAIFramework import ActionAIFramework
from Frameworks.EasyStatsFramework import EasyStatsFramework
from Frameworks.CommonQueryAIFramework import CommonQueryAIFramework
import Frameworks.PlayerStatsPrebuilts as PlayerStatsPrebuilts
import vector

@AI.Team
class Blitzy(ActionAIFramework, EasyStatsFramework, CommonQueryAIFramework):
    def __init__(self):
        ActionAIFramework.__init__(self)
        EasyStatsFramework.__init__(self)
        CommonQueryAIFramework.__init__(self)
        self.player_starting_positions = {}
        self.strategy = [  self.Action_AvoidIncomingBall
                        , self.Action_AttackClosestOpponent
                        , self.Action_CatchIncomingPass
                        , self.Action_GetClosestBall
                        , self.Action_PassBack
                        , self.Action_ReturnToStart
                       ]        
        self.actions[1] = self.strategy
        self.actions[2] = self.strategy
        self.actions[3] = self.strategy
        self.stats = [ PlayerStatsPrebuilts.blitzer, PlayerStatsPrebuilts.blitzer, PlayerStatsPrebuilts.blitzer ]        
        
    def Update(self, ai_input):
        self.SetupStartingPositionsOnFirstUpdate(ai_input)
        return ActionAIFramework.Update(self, ai_input)

    def SetupStartingPositionsOnFirstUpdate(self, ai_input):
        if len(self.player_starting_positions) == 0:    
            for player in ai_input.player_infos:
                self.player_starting_positions[player.number] = player.position


    def Action_AvoidIncomingBall(self, player, instructions, ai_input):
        ball = self.GetClosestInFlightThrownBall(player, ai_input)
        if ball:
            ball_to_player = player.position - ball.position
            distance = ball_to_player.length
            if distance < 40 and self.IsBallGoingToward(ball, player.position):
                instructions.move_target = player.position + ball_to_player
                return True
        return False

    def Action_PassBack(self, player, instructions, ai_input):
        if player.has_ball:
            instructions.is_passing = True
            instructions.pass_target = self.player_starting_positions[player.number]
            instructions.move_target = self.player_starting_positions[player.number]
            return True
        return False

    def Action_CatchIncomingPass(self, player, instructions, ai_input):
        if ai_input.in_flight_ball_infos and not player.has_ball:
            ball = self.GetClosestObject(player.position, [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw == False])
            if ball:
                distance = (ball.position - player.position).length
                ball_to_player = player.position - ball.position
                angel_of_approach = ball_to_player * ball.velocity
                if distance < 20.0 and angel_of_approach > .5:
                    ai_input.in_flight_ball_infos.remove(ball)
                    instructions.move_target = ball.position
                    return True
        return False
    
    def Action_AttackClosestOpponent(self, player, instructions, ai_input):
        #attack
        target = self.GetClosestAttackableOpponent(player, ai_input)
        if player.has_ball and target:
            ai_input.player_infos.remove(target)
            instructions.move_target = target.position
            distance = (target.position - player.position).length
            if distance < 8 * player.throw:
                instructions.is_throwing = True
                instructions.throw_target = target.position
            return True
        return False

    def Action_GetClosestBall(self, player, instructions, ai_input):
        if ai_input.grounded_ball_infos and not player.has_ball:
            ball = self.GetClosestObject(player.position, [ball for ball in ai_input.grounded_ball_infos])
            ai_input.grounded_ball_infos.remove(ball)
            distance = (ball.position - player.position).length
            if distance < 2.0:
                instructions.is_picking = True
            else:
                instructions.move_target = ball.position
            return True
        return False

    def Action_ChargeForward(self, player, instructions, ai_input):
        instructions.move_target = vector.Vector(player.position.x)
        instructions.move_target.y = ai_input.arena_size - self.player_starting_positions[player.number].y
        return True
    
    def Action_ReturnToStart(self, player, instructions, ai_input):
        instructions.move_target = self.player_starting_positions[player.number]
        return True    
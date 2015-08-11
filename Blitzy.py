import Simulation
import ActionAIFramework
import EasyStatsFramework
import PlayerStatsPrebuilts
import vector

class Blitzy(ActionAIFramework.ActionAIFramework, EasyStatsFramework.EasyStatsFramework):
    def __init__(self):
        ActionAIFramework.ActionAIFramework.__init__(self)
        EasyStatsFramework.EasyStatsFramework.__init__(self)
        self.player_starting_positions = {}
        self.actions = [  self.Action_AvoidIncomingBall
                        , self.Action_AttackClosestOpponent
                        , self.Action_CatchIncomingPass
                        , self.Action_GetClosestBall
                        , self.Action_PassBack
                        , self.Action_ReturnToStart
                       ]        
        self.stats = [ PlayerStatsPrebuilts.blitzer, PlayerStatsPrebuilts.blitzer, PlayerStatsPrebuilts.blitzer ]        
        
    def Update(self, ai_input):
        self.SetupStartingPositionsOnFirstUpdate(ai_input)
        return ActionAIFramework.ActionAIFramework.Update(self, ai_input)

    def GetClosestAttackableOpponent(self, player, ai_input):
        target = self.GetClosestObject(player.position, [target for target in ai_input.player_infos if target.team != player.team and target.has_been_hit != True])
        return target

    def GetClosestInFlightThrownBall(self, player, ai_input):
        avoid = self.GetClosestObject(player.position, [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw])
        return avoid

    def SetupStartingPositionsOnFirstUpdate(self, ai_input):
        if len(self.player_starting_positions) == 0:    
            for player in ai_input.player_infos:
                self.player_starting_positions[player.number] = player.position

    def BuildDefaultInstruction(self, player):
        instructions = Simulation.PlayerUpdateInstructions(player.number)
        instructions.move_target = player.position
        instructions.is_moving = True # always moving
        return instructions

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
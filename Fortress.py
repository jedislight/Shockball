import math

import Simulation
import vector
import EasyStatsFramework
import ActionAIFramework
import PlayerStatsPrebuilts

class Fortress(EasyStatsFramework.EasyStatsFramework, ActionAIFramework.ActionAIFramework):
    def __init__(self):
        EasyStatsFramework.EasyStatsFramework.__init__(self)
        ActionAIFramework.ActionAIFramework.__init__(self)
        self.stats = [PlayerStatsPrebuilts.catapault, PlayerStatsPrebuilts.dervish, PlayerStatsPrebuilts.catapault]
        self.mode_fetcher = [self.Action_Dodge, self.Action_GetFieldBall, self.Action_PassBallToTeammate, self.Action_StoreBallAtBase, self.Action_GetClosestBall, self.Action_CircleStart]
        self.mode_turret = [self.Action_Dodge, self.Action_CatchPass, self.Action_ThrowAtNearbyOpponent, self.Action_CircleStart]
        self.mode_solo = [self.Action_Dodge, self.Action_GetClosestBall, self.Action_AttackClosestOpponent]
        
        self.actions[1] = self.mode_turret
        self.actions[2] = self.mode_fetcher
        self.actions[3] = self.mode_turret
        
        self.base_field_percent = 0.1
        self.updates = 0
        
        self.player_starting_positions = {}
        
    def Update(self, ai_input):
        self.updates += 1
        self.SetupStartingPositionsOnFirstUpdate(ai_input)
        my_team_numbers = [player.number if player.number <= 3 else player.number -3 for player in ai_input.player_infos if ai_input.team == player.team]
        if 2 not in my_team_numbers or len(my_team_numbers) == 1:
            self.actions[1] = self.mode_solo
            self.actions[2] = self.mode_solo
            self.actions[3] = self.mode_solo
        return ActionAIFramework.ActionAIFramework.Update(self, ai_input)
                 
    def Action_Dodge(self, player, instructions, ai_input):
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
    
    def Action_GetFieldBall(self, player, instructions, ai_input):
        if ai_input.grounded_ball_infos and not player.has_ball:
            ball = self.GetClosestObject(player.position, [ball for ball in ai_input.grounded_ball_infos if abs(ball.position.y - self.player_starting_positions[player.number].y) >= Simulation.arena_size * self.base_field_percent])
            if ball:
                distance = (ball.position - player.position).length
                if distance < 2.0:
                    instructions.is_picking = True
                else:
                    instructions.move_target = ball.position
                return True
        return False   
    
    def Action_PassBallToTeammate(self, player, instructions, ai_input):
        target = self.GetClosestTeamateWithoutBall(player, ai_input)
        if player.has_ball and target:
            instructions.move_target = target.position
            distance = (target.position - player.position).length
            if distance < 8 * player.throw:
                instructions.is_passing = True
                instructions.pass_target = target.position
            return True
        return False  
    
    def Action_StoreBallAtBase(self, player, instructions, ai_input):
        if player.has_ball:
            target = self.player_starting_positions[player.number]
            instructions.move_target = target
            distance_to_start = (player.position - target).length
            if distance_to_start < Simulation.arena_size * self.base_field_percent:
                instructions.is_passing = True
                instructions.pass_power = 0.0
                instructions.pass_target = target
            return True
        return False    
    
    def Action_CircleStart(self, player, instructions, ai_input):
        frequency = 40.0
        t = self.updates / frequency
        x_offset = math.sin(t / 2 * math.pi) * 10
        y_offset = math.cos(t / 2 * math.pi) * 10
        instructions.move_target = vector.Vector(self.player_starting_positions[player.number].x, self.player_starting_positions[player.number].y)
        if instructions.move_target.y == 0.0:
            instructions.move_target.y += Simulation.arena_size * self.base_field_percent
        else:
            instructions.move_target.y -= Simulation.arena_size * self.base_field_percent
            
        instructions.move_target.x += x_offset
        instructions.move_target.y += y_offset
        return True
    
    def Action_CatchPass(self, player, instructions, ai_input):
        if ai_input.in_flight_ball_infos and not player.has_ball:
            ball = self.GetClosestObject(player.position, [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw == False])
            if ball:
                distance = (ball.position - player.position).length
                ball_to_player = player.position - ball.position
                angel_of_approach = ball_to_player * ball.velocity
                if distance < 20.0 and angel_of_approach > .5:
                    instructions.move_target = ball.position
                    return True
            return False        
        
    def Action_ThrowAtNearbyOpponent(self, player, instructions, ai_input):
        target = self.GetClosestAttackableOpponent(player, ai_input)
        if player.has_ball and target:
            distance = (target.position - player.position).length
            if distance < 8 * player.throw:
                instructions.is_throwing = True
                instructions.throw_target = target.position
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
        if player.has_ball and target:
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
    
    def GetClosestInFlightThrownBall(self, player, ai_input):
        avoid = self.GetClosestObject(player.position, [ball for ball in ai_input.in_flight_ball_infos if ball.is_throw])
        return avoid    
    
    def GetClosestObject(self, origin, objects):
        result = None
        if objects:    
            distances = [(origin - obj.position).length for obj in objects]
            result = objects[distances.index(min(distances))]                    
        return result     
    
    def GetClosestTeamateWithoutBall(self, player, ai_input):
        return self.GetClosestObject(player.position, [player for player in ai_input.player_infos if player.team == ai_input.team and player.has_ball == False])

    def GetClosestAttackableOpponent(self, player, ai_input):
        target = self.GetClosestObject(player.position, [target for target in ai_input.player_infos if target.team != player.team and target.has_been_hit != True])
        return target
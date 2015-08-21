import vector
import random
import math
from AI import *

class LeTiredPlayer(object):
    def __init__(self, position_x, position_y, team):
        self.position = vector.Vector(position_x, position_y)
        self.team = team
    def Update(self):
        pass
    
class Player(object):
    def __init__(self, number):
        self.number = number
        self.position = vector.Vector()
        self.run = 2
        self.pick = 2
        self.throw = 2
        self.stamina = 2
        self.team = 0
        self.has_ball = False
        self.update_per_tired_max = 200
        self.updates_till_tired = random.randint(self.update_per_tired_max * 0.8, self.update_per_tired_max)
        self.has_been_hit = False
        self.move_target = self.position
        
    def SetStats(self, stats):
        assert stats.AreValid()
        self.run = stats.run
        self.pick = stats.pick
        self.throw = stats.throw
        self.stamina = stats.stamina * 2 - 1
        
    def Update(self, player_update_instructions):
        self.updates_till_tired -= 1
        self.move_target = self.position
        #le tired
        if self.updates_till_tired <= 0:
            self.updates_till_tired = self.update_per_tired_max
            self.TakeDamage()
        
        #move
        if self.has_been_hit and self.run != 0:
            if self.team == 0:
                direction = vector.Vector(0,-1)
            else:
                direction = vector.Vector(0,1)
                
            velocity = direction * math.sqrt(self.run)
            self.position = self.position + velocity
            if (self.team == 0 and self.position.y <= 0) or (self.team == 1 and self.position.y >= Simulation.arena_size):
                self.has_been_hit = False

        elif player_update_instructions.is_moving == True and self.run != 0:
            self.move_target= player_update_instructions.move_target
            
            distance = (player_update_instructions.move_target - self.position).length
            velocity = min(math.sqrt(self.run), distance)
            impulse = self.move_target - self.position
            impulse.normalize()
            impulse = impulse * velocity
            self.position = self.position + impulse
        
        self.position.x = max(0.0, self.position.x)
        self.position.x = min(Simulation.arena_size, self.position.x)
        self.position.y = max(0.0, self.position.y)
        self.position.y = min(Simulation.arena_size, self.position.y)        
            
    def TakeDamage(self):
        if self.stamina > 0:
            self.stamina -= 1
            return
        stat_choice = random.randint(0, 2)
        if stat_choice == 0:
            self.run -= 1
            return
        elif stat_choice == 1:
            self.pick -= 1
            return
        elif stat_choice == 2:
            self.throw -= 1
            return
        

class GroundedBall(object):
    def __init__(self, position_x, position_y):
        self.position = vector.Vector(position_x, position_y)
    
    def Update(object):
        pass
    
class InFlightBall(object):
    def __init__(self, target_x , target_y, position_x, position_y, thrower, is_throw, power=1.0):
        power = min(power, 1.0)
        power = max(power, 0.0)
        self.position = vector.Vector(position_x, position_y)
        self.previous_position = self.position
        self.target = vector.Vector(target_x, target_y)
        self.velocity = (self.target - self.position).normalize() * thrower.throw * 2 * power
        self.updates_left = 5
        self.thrower = thrower
        self.is_throw = is_throw
    
    def Update(self):
        #move
        self.previous_position = vector.Vector(self.position.x, self.position.y)
        self.updates_left -= 1
        self.position = self.position + self.velocity
        if self.updates_left <= 0:
            self.velocity = vector.Vector()
        
        self.position.x = max(0, self.position.x)
        self.position.x = min(Simulation.arena_size, self.position.x)
        
        self.position.y = max(0, self.position.y)
        self.position.y = min(Simulation.arena_size, self.position.y)        
        
        if self.position.x in (0.0, Simulation.arena_size) or self.position.y in (0.0, Simulation.arena_size):
            #reflect
            n = vector.Vector()
            if self.position.x == 0.0:
                n = n + vector.Vector(1,0)
            if self.position.x == Simulation.arena_size:
                n = n + vector.Vector(-1, 0)
            if self.position.y == 0.0:
                n = n + vector.Vector(0,-1)
            if self.position.y == Simulation.arena_size:
                n = n + vector.Vector(0, 1)
                
            n.normalize()
            
            self.velocity = self.velocity -  n * ((self.velocity * n) * 2)
        
class Simulation(object):
    arena_size = 100  
    def __init__(self, team_0_ai, team_1_ai):
        self.update_count = 0
        self.winning_team_won_on_update = -1
        
        #ai store
        self.ai = [team_0_ai, team_1_ai]
        
        #set final state
        self.winning_team = -1
        
        #set teams
        self.players = [Player(1),Player(2),Player(3),Player(4),Player(5),Player(6)]#6
        self.players[0].team = 0
        self.players[1].team = 0
        self.players[2].team = 0
        self.players[3].team = 1
        self.players[4].team = 1
        self.players[5].team = 1
        
        #setup stats
        self.players[0].SetStats(team_0_ai.GetPlayerStats(1))
        self.players[1].SetStats(team_0_ai.GetPlayerStats(2))
        self.players[2].SetStats(team_0_ai.GetPlayerStats(3))
        self.players[3].SetStats(team_1_ai.GetPlayerStats(1))
        self.players[4].SetStats(team_1_ai.GetPlayerStats(2))
        self.players[5].SetStats(team_1_ai.GetPlayerStats(3))      
        
        #set positions
        self.players[0].position = vector.Vector(.25*self.arena_size, 0)
        self.players[1].position = vector.Vector(.50*self.arena_size, 0)
        self.players[2].position = vector.Vector(.75*self.arena_size, 0)
        
        self.players[3].position = vector.Vector(.25*self.arena_size, self.arena_size)
        self.players[4].position = vector.Vector(.50*self.arena_size, self.arena_size)
        self.players[5].position = vector.Vector(.75*self.arena_size, self.arena_size)
        
        #set balls
        self.grounded_balls = [
            GroundedBall(.50*self.arena_size, .10*self.arena_size),
            GroundedBall(.25*self.arena_size, .50*self.arena_size),
            GroundedBall(.50*self.arena_size, .50*self.arena_size),
            GroundedBall(.75*self.arena_size, .50*self.arena_size),
            GroundedBall(.50*self.arena_size, .90*self.arena_size)
        ]
        
        #setup inflight balls
        self.in_flight_balls = []
        
        #setup le tired players
        self.le_tired_players = []
        
    def Update(self):
        self.update_count += 1
        #update everything
        for updateable in self.grounded_balls + self.in_flight_balls:
            updateable.Update()
            
        players_instructions = dict()
        for player in self.players:
            players_instructions[player] = PlayerUpdateInstructions(player.number)
            
        #do AI here
        for team in [0,1]:
            ai_input = AIInput(self, team)
            ai_output = self.ai[team].Update(ai_input)
            for player_update_instruction in ai_output.player_update_instructions:
                for player in self.players:
                    if player.number == player_update_instruction.number and player.team == team:        
                        players_instructions[player] = player_update_instruction

        for player in self.players:
            player.Update(players_instructions[player])
        
        #pick
        for player in self.players:
            if players_instructions[player].is_picking and player.has_been_hit == False:
                if len(self.grounded_balls) > 0:
                    nearest_ball = None
                    nearest_distance = self.arena_size * 10
                    for grounded_ball in self.grounded_balls:
                        distance_to_player_for_current_grounded_ball = (player.position - grounded_ball.position).length
                        if distance_to_player_for_current_grounded_ball < nearest_distance:
                            nearest_distance = distance_to_player_for_current_grounded_ball
                            nearest_ball = grounded_ball
                    if nearest_distance <= 2.0:
                        #close enough to pick yay!
                        if random.randint(1,20) <= player.pick ** player.pick:
                            #success
                            player.has_ball = True
                            self.grounded_balls.remove(nearest_ball)
        #pass/throw
        for player in self.players:
            if player.has_ball == False:
                continue
            instructions = players_instructions[player]
            if instructions.is_throwing or instructions.is_passing:                
                target = instructions.throw_target
                power = instructions.throw_power
                if instructions.is_passing:
                    target = instructions.pass_target
                    power = instructions.pass_power                  
                
                player.has_ball = False
                ball = InFlightBall(target.x, target.y, player.position.x, 
                                   player.position.y, player, instructions.is_throwing, power)
                self.in_flight_balls.append(ball)
        
        #ball grounding
        for ball in self.in_flight_balls[:]:
            if ball.updates_left <= 0:
                self.in_flight_balls.remove(ball)
                self.grounded_balls.append(GroundedBall(ball.position.x, ball.position.y))
        
        #collision!
        for ball in self.in_flight_balls[:]:
            nearest_player = None
            nearest_distance = self.arena_size * 10 # really big
            for player in self.players:
                if ball.thrower != player:
                    distance = Simulation.DistanceToLineSegment(ball.position, ball.previous_position, player.position)
                    if distance < nearest_distance:
                        nearest_player = player
                        nearest_distance = distance
            player = nearest_player
            if player != None and nearest_distance <= 2:
                #collision!
                if player.has_been_hit or player.has_ball:
                    self.grounded_balls.append(GroundedBall(ball.position.x, ball.position.y))
                elif ball.is_throw:
                    player.TakeDamage()
                    player.has_been_hit = True
                    self.grounded_balls.append(GroundedBall(ball.position.x, ball.position.y))
                else:
                    player.has_ball = True
                    
                self.in_flight_balls.remove(ball)
        
        #player elimination
        for player in self.players[:]:
            if player.run <=0 or player.pick <=0 or player.throw <= 0:
                self.players.remove(player)
                self.le_tired_players.append(LeTiredPlayer(player.position.x, player.position.y, player.team))
                
        #check for winner!
        if self.winning_team == -1:
            if len(self.players) == 0:
                self.winning_team = 2
            else:
                team = self.players[0].team
                is_going_still = False
                for player in self.players:
                    if player.team != team:
                        is_going_still = True
            
                if not is_going_still:
                    self.winning_team_won_on_update = self.update_count
                    self.winning_team = team
                    
    @classmethod
    def DistanceToLineSegment(cls, v, w, p):
        l2 = (v-w).length
        l2 = l2** 2
        
        if l2 == 0.0:
            return (p - v).length
        
        t = ( (p-v) * (w-v) ) / l2
        if t < 0.0:
            return (p-v).length
        elif t > 1.0:
            return (p-w).length
        
        projection = v + (w-v) * t
        return (p-projection).length
import vector

class AI(object):
    team = []
    def __init__(self):
        pass
    
    def Update(self, ai_input):
        return AIOutput()
    
    def GetPlayerStats(self, player_number):
        """player number will be 1,2, or 3"""
        return PlayerStats() # default stats for any player
    
    @classmethod
    def Team(cls, other):
        cls.team.append(other)
    
    

class AIInput(object):
    def __init__(self, simulation, team):
        self.arena_size = simulation.arena_size
        
        self.team = team 
        
        self.player_infos = []
        for player in simulation.players:
            self.player_infos.append(PlayerInfo(player, team == player.team))
            
        self.grounded_ball_infos = []
        for ball in simulation.grounded_balls:
            self.grounded_ball_infos.append(GroundedBallInfo(ball))
            
        self.in_flight_ball_infos = []
        for ball in simulation.in_flight_balls:
            self.in_flight_ball_infos.append(InFlightBallInfo(ball))
            
class AIOutput(object):
    def __init__(self):
        self.player_update_instructions = []

class PlayerStats(object):
    def __init__(self):
        self.run = 2
        self.throw = 2
        self.pick = 2
        self.stamina = 2
    
    def AreValid(self):
        stats = [self.run, self.throw, self.pick, self.stamina]
        min_stat = min(stats)
        max_stat = max(stats)
        total_stat = sum(stats)
        return (min_stat == 1 and max_stat == 3 and total_stat == 8) or (min_stat == 2 and max_stat == 2)

class InFlightBallInfo(object):
    def __init__(self, in_flight_ball):
        self.position = in_flight_ball.position
        self.velocity = in_flight_ball.velocity
        self.thrower = in_flight_ball.thrower
        self.is_throw = in_flight_ball.is_throw    

class GroundedBallInfo(object):
    def __init__(self, grounded_ball):
        self.position = grounded_ball.position

class PlayerInfo(object):
    def __init__(self, player, is_team_member):
        self.position = player.position
        self.team = player.team
        self.has_ball = player.has_ball
        self.has_been_hit = player.has_been_hit
        self.number = player.number
        
        if is_team_member:#TODO
            self.run = player.run
            self.pick = player.pick
            self.throw = player.throw
            self.stamina = player.stamina
        else:
            self.run = None
            self.pick = None
            self.throw = None
            self.stamina = None     

class PlayerUpdateInstructions(object):
    def __init__(self, number):
        self.move_target = vector.Vector()
        self.is_moving = False
        
        self.is_picking = False
        
        self.throw_target = vector.Vector()
        self.is_throwing = False
        self.throw_power = 1.0
        
        self.pass_target = vector.Vector()
        self.is_passing = False
        self.pass_power = 1.0
        
        self.number = number
        
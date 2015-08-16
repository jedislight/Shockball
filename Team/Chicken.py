from AI import AI
from Frameworks.ActionAIFramework import ActionAIFramework
from Frameworks.EasyStatsFramework import EasyStatsFramework
from Frameworks.CommonQueryAIFramework import CommonQueryAIFramework
import Frameworks.PlayerStatsPrebuilts as PlayerStatsPrebuilts
import vector

@AI.Team
class Chicken(ActionAIFramework, EasyStatsFramework, CommonQueryAIFramework):
    def __init__(self):
        ActionAIFramework.__init__(self)
        EasyStatsFramework.__init__(self)
        CommonQueryAIFramework.__init__(self)
        self.stats = [PlayerStatsPrebuilts.blitzer, PlayerStatsPrebuilts.blitzer, PlayerStatsPrebuilts.blitzer] * 3
        logic = [self.Action_GetBallIfClosest, self.Action_AvoidEverything]
        self.actions[1] = logic
        self.actions[2] = logic
        self.actions[3] = logic
        
    def Action_GetBallIfClosest(self, player, instructions, ai_input):
        closest = self.GetClosestObject(player.position, [p for p in ai_input.player_infos if p.number != player.number] + ai_input.grounded_ball_infos + ai_input.in_flight_ball_infos)
        closest_opponent = self.GetClosestAttackableOpponent(player, ai_input)
        if not player.has_ball and closest and closest in ai_input.grounded_ball_infos and self.Distance(closest_opponent, player) > 25:
            instructions.move_target = closest.position
            instructions.is_picking = True
            return True
        return False
    
    def Action_AvoidEverything(self, player, instructions, ai_input):
        bad_things = ai_input.in_flight_ball_infos + self.GetOpponents(ai_input)
        closest_bad_thing = self.GetClosestObject(player.position, bad_things)
        corners = [vector.Vector(-0.1,-0.1), vector.Vector(-0.1, ai_input.arena_size+0.1), vector.Vector(ai_input.arena_size+0.1, -0.1), vector.Vector(ai_input.arena_size+0.1, ai_input.arena_size+0.1)]
        aways = [player.position - bad_thing.position for bad_thing in bad_things] + [player.position - corner for corner in corners]
        away_lengths = [away.length for away in aways]
        aways = [away.normalize() * (ai_input.arena_size * 1.5 - length) for away, length in zip(aways,away_lengths)]
        run_here = vector.Vector()
        for away in aways:
            run_here = run_here + away
            
        instructions.move_target = run_here
        return True
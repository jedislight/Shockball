import Simulation
import vector

class ActionAIFramework(Simulation.AI):
    def __init__(self):
        self.actions = {}
            
    def Update(self, ai_input):
        output = Simulation.AIOutput()
    
        my_team = [player for player in ai_input.player_infos if player.team == ai_input.team and player.has_been_hit == False]
        for player in my_team:            
            instructions = self.BuildDefaultInstruction(player)
            number = player.number
            if number > 3:
                number -= 3
            action_params = (player, instructions, ai_input)    
            for action in self.actions[number]:
                if action(*action_params):
                    break
    
            output.player_update_instructions.append(instructions)
    
        return output

    def BuildDefaultInstruction(self, player):
        instructions = Simulation.PlayerUpdateInstructions(player.number)
        instructions.move_target = player.position
        instructions.is_moving = True # always moving
        return instructions
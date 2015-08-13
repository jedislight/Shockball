'''
Action based AIFramework - setup self.actions as a dictionary for 1-3 for your players with arrays of Action methods taking paramaters (player, instructions, ai_input). No need to define Update
'''
from AI import AI
from AI import AIOutput
from AI import PlayerUpdateInstructions
import vector

class ActionAIFramework(AI):
    def __init__(self):
        self.actions = {}
            
    def Update(self, ai_input):
        output = AIOutput()
    
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
        instructions = PlayerUpdateInstructions(player.number)
        instructions.move_target = player.position
        instructions.is_moving = True # always moving
        return instructions
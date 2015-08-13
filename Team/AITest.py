from AI import AI
from AI import AIOutput
from AI import PlayerUpdateInstructions
import vector

@AI.Team
class AITest(AI):
    def __init__(self):
        pass
    def Update(self, ai_input):
        output = AIOutput()
        ins = PlayerUpdateInstructions(1)
        ins.is_moving = True
        ins.move_target = vector.Vector(50.0,50.0)
        output.player_update_instructions.append(ins)
        return output
import Simulation
import vector

class AITest(Simulation.AI):
    def __init__(self):
        pass
    def Update(self, ai_input):
        output = Simulation.AIOutput()
        ins = Simulation.PlayerUpdateInstructions(1)
        ins.is_moving = True
        ins.move_target = vector.Vector(50.0,50.0)
        output.player_update_instructions.append(ins)
        return output
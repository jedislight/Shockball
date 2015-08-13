# Shockball
Competitive AI programming in a dodge ball like game. Write your python to control your team and seek victory.

# Shockball Game Rules
Shockball is a 3 on 3 competitive team sport. The goal of the game is to knock out your opponents by hitting them with an electrically charged ball. The game is played in a square walled playing field 100 units wide. Each team starts with all of its players along opposite walls. Five balls wait at the beginging of play. One ball near each team, and Three balls in the center of the two teams. Each player is described by 4 stats:
* Run : how fast the player can move
* Throw : how fast and how far the player can throw
* Pick : how quickly a player can pickup a grounded ball
* Stamina : how many shocks a player can absorb before other stats degrade

Every time a player is hit they must run back to their starting wall before re-entering play. Also getting shocked reduced one stat by one point. If stamina is not 0,  stamina will be reduced, otherwise another stat will be selected unpredictably. Over time a player will fatigue and start loosing stats naturally - no individual game can last forever.

# Creating a Team
* Create a new python file next to the main_window.py with the name of your team
* Create a class that inherits from Simulation.AI
* Decorate your class with @AI.Team
* Overload the Update() method to build your own AIOutput object based on the state of the AIInupt object
* Overload the GetPlayerStats() method to build your player stats for your 1,2, & 3 players

The AIOutput object needs to be provided a PlayerUpdateInstructions object for each player. The PlayerUpdateInstructions object supports 4 actions:
* is_moving - when true moves to the move_target position
* is_passing - when true passes (harmless) to the pass_target position, pass_power can be set from 0.0 -> 1.0 to scale back the strength of the pass, defaults to full power
* is_throwing - when true throws (harmful) to the throw_target position, throw_power can be set from 0.0 -> 1.0 to scale back the strength of the throw, defaults to full power

# Frameworks
Frameworks are helpful partially implemented AI Teams that can greatly streamline common development tasks. Check out Team/Basic - the whole team was written in about 5 minutes and is less than 50 lines of code

# Running a Game
* python main_window.py team1Name team2Name [-options]
  * -slow_sim : runs the simulation at 4 fps for easy debugging
  * -quick_sim : runs the simulation to completion as fast as possible then draws the result. Good for quick win ratio gauging
  * -draw_target : draws the move targets of the players

# Road-Map
* See Issues https://github.com/jedislight/Shockball/issues
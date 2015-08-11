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
* Overload the Update() method to build your own AIOutput object based on the state of the AIInupt object
* Overload the GetPlayerStats() method to build your player stats for your 1,2, & 3 players

# Running a Game
* python main_window.py team1Name team2Name [-options]
  * -slow_sim : runs the simulation at 4 fps for easy debugging
  * -quick_sim : runs the simulation to completion as fast as possible then draws the result. Good for quick win ratio gauging
  * -draw_target : draws the move targets of the players

# Road-Map
* AI import from subfolder
* CLI option for framerate as value
* Tutorial Teams

# Complete
* Clamp velocity of move to distance needed to reach target
* Limit AI outputs from effecting other team's players
* Fix ball duplication and flightless ball buginess
* Bulk simulation option
* Visual difference between team members
* Data drive AI module loading
* Allow AI to set stats of players during simulation construction
* Ball flight w/ throw 1 should be the only speed that can be outrun, and only by a run 3
* Balls locked into play field with bounce
* Players locked into play field
* -draw_targets available to show player destinations
* Frame rate adjusted to be more viewable
* In flight balls made frame based instead of time based
* Picking now has squared growth (IE pick chance per frame == 1/20, 4,20, 9/20) value to encourage high pick scores
* Run now has root growth (IE runspeed == 1, 1.4, 1.7)
* In flight balls now do line segment collision to prevent tunneling
* Python 3.X
* Populate Readme with actual description of use and simulation rules
* Stat prebuilts with fancy names
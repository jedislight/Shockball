from tkinter import *
import os
import inspect
import importlib
import argparse
import random

from Simulation import Simulation
from AI import AI
import Team

class Controller(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description="Competitive AI programming in a dodge ball like game.")
        parser.add_argument("teams", nargs="*", help="the 2 teams to face off")
        speed_group = parser.add_mutually_exclusive_group()
        speed_group.add_argument("--quick_sim", "-q", action="store_true", help="Simulates games as fast as possible")
        speed_group.add_argument("--fps", "-f", action="store", type=int, default=20, help="Sets simulation speed")
        parser.add_argument("--draw_target", "-d", action="store_true", help="Draws the destination of players for debugging")
        parser.add_argument("--bouncy_ball", action="store_true", help="Adds a bouncy ball to the game for debugging")
        args = parser.parse_args(os.sys.argv[1:])
        
        self.master = Tk()      
        
        self.fps = args.fps    
        self.quick_sim = args.quick_sim
        self.draw_target = BooleanVar(master=self.master, value=args.draw_target)
        self.bouncy_ball = args.bouncy_ball
        self.wins = [0,0,0]
        
        self.simulation = None
        self.all_teams = self.ImportTeams(args)
        self.team_0_ai = AI.team[0]()
        self.team_1_ai = AI.team[1]()

        self.menu_bar = Menu(self.master)
            
        self.shockball_menu = Menu(self.menu_bar)
        self.shockball_menu.add_command(label="New Game", command=self.NewGame, accelerator="F2")
        self.shockball_menu.add_checkbutton(label="Draw Targets", onvalue = True, offvalue = False, variable=self.draw_target)
        self.master.bind_all("<F2>", self.NewGame)
        
        self.menu_bar.add_cascade(label = "Shockball", menu=self.shockball_menu)
        
        self.master.config(menu = self.menu_bar)
        
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        
        self.NewGame()

    def ImportTeams(self, args):
        if len(args.teams) ==2:
            importlib.import_module("Team.{0}".format(args.teams[0]))
            if len(AI.team) > 1:
                assert False, "Found more than one team in {0}".format(args.teams[0])
            if len(AI.team) < 1:
                assert False, "Found no team in {0}. Did you remember to add the @AI.Team decorator?".format(args.teams[0])        
            importlib.import_module("Team.{0}".format(args.teams[1]))
            if len(AI.team) > 2:
                assert False, "Found more than one team in {0}".format(args.teams[1])
            if len(AI.team) < 2:
                assert False, "Found no team in {0}. Did you remember to add the @AI.Team decorator?".format(args.teams[1])    
            return False
        else:
            teams = []
            for _, _, files in os.walk("Team"):
                for file in files:
                    if "__" not in file and file.endswith(".py"):
                        teams.append( file.replace(".py", "") )
            random.shuffle(teams)
            for team in teams:
                importlib.import_module("Team.{0}".format(team))
            return True
        
        
    def NewGame(self, event=None):
        if self.all_teams:
            winner = self.simulation.winning_team if self.simulation else 0
            if winner == 2:#tie
                winner = 0#encumbant
            champion = AI.team.pop(winner)
            random.shuffle(AI.team)
            AI.team.insert(0, champion)
            self.team_0_ai = AI.team[0]()
            self.team_1_ai = AI.team[1]()            
            if winner != 0:
                self.wins=[0,0,0]
            
        self.simulation = Simulation(self.team_0_ai, self.team_1_ai)
        
        if self.bouncy_ball:
            ball = AI.InFlightBall(20.0, 41.0, 50.0,50.0, self.simulation.players[0], True)
            ball.updates_left = 9999            
            self.simulation.in_flight_balls.append(ball)        
        return
        
    def MainLoop(self):
        self.Update()
        self.master.mainloop()
        
    def Update(self):
        if self.quick_sim:
            while self.simulation.winning_team < 0:
                self.simulation.Update()
            self.wins[self.simulation.winning_team] += 1
            self.DrawSimulation()
            self.NewGame()
        else:
            self.DrawSimulation()
            self.simulation.Update()
            if self.simulation.winning_team != -1 and self.simulation.winning_team_won_on_update == self.simulation.update_count:
                self.wins[self.simulation.winning_team] += 1
        
        self.master.after(int(1000.0/self.fps),self.Update)
            
    def DrawSimulation(self):
        self.w.delete(ALL)
        c = "white"
        if self.simulation.winning_team == 1:
            c = "cyan"
        if self.simulation.winning_team == 0:
            c = "pink"
        self.w.create_rectangle(0,0,Simulation.arena_size * 6, Simulation.arena_size * 6, fill = c)
        self.w.create_text(2,2, anchor = NW, text = "Red(" + self.team_0_ai.__class__.__name__ +"):" + str(self.wins[0]) + " Blue("+self.team_1_ai.__class__.__name__+"): " + str(self.wins[1]) + " Draw: " + str(self.wins[2]))
        for player in self.simulation.le_tired_players:
            color = "pink"
            if player.team == 1:
                color ="cyan"
            self.w.create_rectangle(player.position.x*5 - 7.5, player.position.y*5 - 7.5, player.position.x*5 + 7.5, player.position.y*5 + 7.5, fill=color)
            self.w.create_line(player.position.x*5 - 7.5, player.position.y*5 - 7.5, player.position.x*5 + 7.5, player.position.y*5 + 7.5)
            self.w.create_line(player.position.x*5 + 7.5, player.position.y*5 - 7.5, player.position.x*5 - 7.5, player.position.y*5 + 7.5)
        for player in self.simulation.players:
            color = "pink"
            if player.team == 1:
                color ="cyan"
            self.w.create_rectangle(player.position.x*5 - 7.5, player.position.y*5 - 7.5, player.position.x*5 + 7.5, player.position.y*5 + 7.5, fill=color)
            self.w.create_text((player.position.x-2.5) * 5, player.position.y * 5, text = str(player.number))
            if player.has_ball:
                self.w.create_rectangle(player.position.x*5, player.position.y*5 - 2.5, player.position.x*5 + 5, player.position.y*5 + 2.5)
            if self.draw_target.get():
                self.w.create_line(player.position.x*5, player.position.y*5, player.move_target.x*5, player.move_target.y*5, fill=color)
        for ball in self.simulation.grounded_balls:
                self.w.create_rectangle(ball.position.x*5 - 2.5, ball.position.y*5 - 2.5, ball.position.x*5 + 2.5, ball.position.y*5 + 2.5)
        for ball in self.simulation.in_flight_balls:
            color = 'pink'
            if ball.thrower.team == 1:
                color = 'cyan'
            if ball.is_throw:
                color = 'black'
            self.w.create_rectangle(ball.position.x*5 - 2.5, ball.position.y*5 - 2.5, ball.position.x*5 + 2.5, ball.position.y*5 + 2.5, fill = color)

if __name__ == "__main__":
    controller = Controller()
    controller.MainLoop()
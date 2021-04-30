from .arcade_button import ArcadeButton
from .display import Display
from .score import Score

#Player-Class
class Player(object):
    def __init__(self, number, arcade_button, display, score):
        self.number = number
        self.active = False
        self.arcade_button = arcade_button
        self.display = display
        self.score = score

    #wird ein Button gedrückt, passiert folgendes
    def buttonWasPushed(self, player_number): 
         
        global number
        number += 1
        print("\n", number, "x pushed")

        player = self
        argument = [gameTable.status, player]
        playerSwitcher(argument)
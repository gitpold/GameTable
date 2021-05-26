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
        self.counter = 0

    def is_active(self):
        return self.active

    def get_number(self):
        return self.number

    def get_all(self):
        return {
            'number': self.number,
            'active': self.active,
            'button': self.arcade_button.get_all(),
            'display': self.display.get_all(),
            'score': self.score.get_all()
        }

    def set_active(self, active):
        self.active = active
        print("player " + str(self.number) + ": " + str(self.active))
        if active:
            self.arcade_button.switch_on()
            self.display.set_text('Player ' + str(self.number))
        else:
            self.arcade_button.switch_off()
            self.display.set_text('        ')

    def toggle_active(self):
        self.set_active(not self.active)

    def clear_counter(self):
        self.counter = 0

    def increase_counter(self):
        self.counter += 1

    #wird ein Button gedrückt, passiert folgendes
    def buttonWasPushed(self, player_number): 
         
        global number
        number += 1
        print("\n", number, "x pushed")

        player = self
        argument = [gameTable.status, player]
        playerSwitcher(argument)
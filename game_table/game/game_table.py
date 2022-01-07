# imports

from hashlib import new
import RPi.GPIO as GPIO

import time
import random
import threading

from .player import Player
from .arcade_button import ArcadeButton
from .display import Display
from .score import Score

#GameTable-Class
class GameTable(object):
    def __init__(self, players, big_button, seg):
        self.players = players
        self.big_button = big_button
        self.status = 'PLAYER_SELECTION' # available stati: PLAYER_SELECTION, GAME_MODE_SELECTION, GAME_PLAYING, GAME_OVER 
        self.mode = None 
        self.seg = seg
        self.timer = None


    # getters for rest endpoints

    def get_all(self):
        return {
            'players': self.get_players(), 
            'big_button': self.big_button.get_all(),
            'status': self.status,
        }

    def get_players(self):
        return list(map(Player.get_all, self.players))

    def get_active_players(self):
        return list(map(Player.get_all, filter(Player.is_active, self.players)))

    def get_player(self, id):
        return next(filter(lambda player: player.get_number() == int(id), self.players)).get_all()


    # helper getters

    def get_player_by_gpio(self, gpio):
        return next((x for x in self.players if x.arcade_button.button == gpio), None)

    def get_player_by_number(self, number):
        return next((x for x in self.players if x.number == number), None)


    # global clears / animations / etc.

    def clear_all(self):
        for player in self.players:
            player.arcade_button.switch_off()
            player.display.set_text('        ')

    def clear_all_buttons(self):
        for player in self.players:
            player.arcade_button.switch_off()

    def clear_all_displays(self):
        for player in self.players:
            player.display.set_text('        ')


    # handle big button press

    def big_button_pressed(self):

        if self.status == 'PLAYER_SELECTION':
            if len(self.get_active_players()) > 0:
                self.set_game_mode_selection()

        elif self.status == 'GAME_MODE_SELECTION':
            if self.mode != None:
                self.status = 'GAME_PLAYING'
                self.clear_all()
                self.start_game()
                print("GAME_PLAYING")

        elif self.status == 'GAME_OVER':
            self.status = 'PLAYER_SELECTION'
            self.clear_all()
            for player in filter(Player.is_active, self.players):
                player.toggle_active()
                player.toggle_active()

            print("PLAYER_SELECTION")

        self.big_button.switch_off()

        # TODO


    # handle game mode selection

    def set_game_mode_selection(self):
        self.clear_all()

        self.players[0].display.set_text('GAME 1')
        self.players[1].display.set_text('GAME 2')
        self.players[2].display.set_text('GAME 3')
        self.players[3].display.set_text('GAME 4')
        self.players[4].display.set_text('GAME 5')
        self.players[5].display.set_text('GAME 6')
        self.players[6].display.set_text('GAME 7')
        self.players[7].display.set_text('GAME 8')


        if self.mode == 'GAME_1':
            self.players[0].arcade_button.switch_on()

        if self.mode == 'GAME_2':
            self.players[1].arcade_button.switch_on()

        if self.mode == 'GAME_3':
            self.players[2].arcade_button.switch_on()

        if self.mode == 'GAME_4':
            self.players[3].arcade_button.switch_on()

        if self.mode == 'GAME_5':
            self.players[4].arcade_button.switch_on()

        if self.mode == 'GAME_6':
            self.players[5].arcade_button.switch_on()

        if self.mode == 'GAME_7':
            self.players[6].arcade_button.switch_on()

        if self.mode == 'GAME_8':
            self.players[7].arcade_button.switch_on()

        print("GAME_MODE_SELECTION")

        self.status = 'GAME_MODE_SELECTION'



    # handle every button press of a player while selection or while playing
    
    def player_button_pressed(self, number):

        if self.status == 'PLAYER_SELECTION':
            self.get_player_by_number(number).toggle_active()

            if len(self.get_active_players()) > 0:
                self.big_button.switch_on()
            else:
                self.big_button.switch_off()

        elif self.status == 'GAME_MODE_SELECTION':

            self.clear_all_buttons()

            if number == 1:
                self.mode = 'GAME_1'
                self.players[0].arcade_button.switch_on()
            elif number == 2:
                self.mode = 'GAME_2'
                self.players[1].arcade_button.switch_on()
            elif number == 3:
                self.mode = 'GAME_3'
                self.players[2].arcade_button.switch_on()
            elif number == 4:
                self.mode = 'GAME_4'
                self.players[3].arcade_button.switch_on()
            elif number == 5:
                self.mode = 'GAME_5'
                self.players[4].arcade_button.switch_on()
            elif number == 6:
                self.mode = 'GAME_6'
                self.players[5].arcade_button.switch_on()
            elif number == 7:
                self.mode = 'GAME_7'
                self.players[6].arcade_button.switch_on()
            elif number == 8:
                self.mode = 'GAME_8'
                self.players[7].arcade_button.switch_on()
            else:
                self.mode = None

            print(self.mode)

            if self.mode != None:
                self.big_button.switch_on()
            else:
                self.big_button.switch_off()


        elif self.status == 'GAME_PLAYING':
        
            if self.mode == 'GAME_1':
                self.game_1_click(number)

            elif self.mode == 'GAME_2':
                self.game_2_click(number)

            elif self.mode == 'GAME_3':
                self.game_3_click(number)

            elif self.mode == 'GAME_4':
                print("todo")
                # TODO
        
            elif self.mode == 'GAME_5':
                print("todo")
                # TODO
            
            elif self.mode == 'GAME_6':
                print("todo")
                # TODO
            
            elif self.mode == 'GAME_7':
                print("todo")
                # TODO
            
            elif self.mode == 'GAME_8':
                print("todo")
                # TODO



    # helper methods to handle player button presses for each different game mode

    def game_1_click(self, number):
        print("test " + str(number))

        player = self.get_player_by_number(number)
        player.increase_counter()
        player.display.set_text(player.counter)


    def game_2_click(self, number):
        print("game 2")

        self.timer.cancel()
        self.timer = threading.Timer(1.0, self.game_2_over)
        self.timer.start()

        player = self.get_player_by_number(number)
        player.arcade_button.switch_off()

        active_players = list(filter(Player.is_active, self.players))

        print(active_players)

        active_players.remove(player)

        print(active_players)

        new_player = random.choice(active_players)

        print(new_player)

        new_player.arcade_button.switch_on()


    def game_3_click(self, number):
        print("todo")

    
    def game_4_click(self, number):
        print("todo")

    
    def game_5_click(self, number):
        print("todo")

    
    def game_6_click(self, number):
        print("todo")

    
    def game_7_click(self, number):
        print("todo")

    
    def game_8_click(self, number):
        print("todo")



    # handle game start

    def start_game(self):

        self.clear_all()

        for player in filter(Player.is_active, self.players):
            player.clear_counter()


        # GAME 1: 
        #
        # every player is pressing his button as often as possible in 10 seconds, player wiht the highest count wins
        #
        if self.mode == 'GAME_1':

            for player in filter(Player.is_active, self.players):
                player.display.set_text(player.counter)

            gameThread = threading.Thread(target=self.game_1_thread, args=())
            gameThread.start()


        # GAME 2:
        #
        # todo
        #
        elif self.mode == 'GAME_2':

            self.timer = threading.Timer(1.0, self.game_2_over)
            self.timer.start()

            active_players = list(filter(Player.is_active, self.players))

            new_player = random.choice(active_players)
            new_player.arcade_button.switch_on()

        # GAME 3:
        #
        #
        #
        elif self.mode == 'GAME_3':

            print("Not yet implemented")

        # GAME 4:
        #
        #
        #
        elif self.mode == 'GAME_4':

            print("Not yet implemented")

        # GAME 5:
        #
        #
        #
        elif self.mode == 'GAME_5':

            print("Not yet implemented")

        # GAME 6:
        #
        #
        #  
        elif self.mode == 'GAME_6':

            print("Not yet implemented")

        # GAME 7:
        #
        #
        #
        elif self.mode == 'GAME_7':

            print("Not yet implemented")

        # GAME 8:
        #
        #
        #
        elif self.mode == 'GAME_8':

            print("Not yet implemented")



    # needed helper threads and functions for the different games

    def game_1_thread(self):

        time.sleep(10)

        active_players = list(filter(Player.is_active, self.players))

        active_players.sort(key=lambda player: player.counter, reverse=True)

        active_players[0].arcade_button.switch_on()

        self.status = 'GAME_OVER'


    def game_2_over(self):

        self.status = 'GAME_OVER'


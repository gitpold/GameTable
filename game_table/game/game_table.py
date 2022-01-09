# imports

from hashlib import new
import RPi.GPIO as GPIO

import time
import random
import threading

from .constants import GAME_MODE, GAME_STATE

from .player import Player
from .arcade_button import ArcadeButton
from .display import Display
from .score import Score


#GameTable-Class
class GameTable(object):
    def __init__(self, players, big_button, seg):
        self.players = players
        self.big_button = big_button
        self.state = GAME_STATE.PLAYER_SELECTION # available stati: PLAYER_SELECTION, GAME_MODE_SELECTION, GAME_PLAYING, GAME_OVER
        self.mode = None 
        self.seg = seg
        self.timer = None


    # getters for rest endpoints

    def get_all(self):
        return {
            'players': self.get_players(), 
            'big_button': self.big_button.get_all(),
            'state': self.state.name,
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


    # helper setters

    def set_game_state(self, state):
        self.state = state
        print("Game state:", state.name)

    def set_game_mode(self, mode):
        self.mode = mode
        if mode != None:
            print("Game mode:", mode.name)
        else:
            print("Game mode: None")


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

        self.clear_all()
        self.big_button.switch_off()

        # if current state is PLAYER_SELECTION
        if self.state == GAME_STATE.PLAYER_SELECTION:
            if len(self.get_active_players()) > 0:
                self.set_game_state(GAME_STATE.GAME_MODE_SELECTION)
         
                for game_mode in GAME_MODE:
                     self.players[game_mode.value].display.set_text(game_mode.name)

                if self.mode != None:
                     self.players[self.mode.value].arcade_button.switch_on()
                     self.big_button.switch_on()


        # if current state is GAME_MODE_SELECTION
        elif self.state == GAME_STATE.GAME_MODE_SELECTION:
            if self.mode != None:
                self.set_game_state(GAME_STATE.GAME_PLAYING)
                self.state = GAME_STATE.GAME_PLAYING
                self.start_game()

        # if current state is GAME_OVER
        elif self.state == GAME_STATE.GAME_OVER:
            self.set_game_state(GAME_STATE.PLAYER_SELECTION)
            for player in filter(Player.is_active, self.players):
                player.toggle_active()
                player.toggle_active()

            if len(self.get_active_players()) > 0:
                self.big_button.switch_on()

        # TODO
        # but what?



    # handle every button press of a player while selection or while playing
    
    def player_button_pressed(self, number):

        # if current state is PLAYER_SELECTION
        if self.state == GAME_STATE.PLAYER_SELECTION:
            self.get_player_by_number(number).toggle_active()

            if len(self.get_active_players()) > 0:
                self.big_button.switch_on()
            else:
                self.big_button.switch_off()

        # if current state is GAME_MODE_SELECTION
        elif self.state == GAME_STATE.GAME_MODE_SELECTION:

            if self.mode != GAME_MODE(number - 1):

                self.clear_all_buttons()

                if number >= 1 and number <= 8:         
                    # valid game mode selected
                    self.set_game_mode(GAME_MODE(number - 1))
                    self.players[number - 1].arcade_button.switch_on()
                    self.big_button.switch_on()
                    
                else:
                    # no valid game mode selected
                    self.set_game_mode(None)                           
                    self.big_button.switch_off()

        # if current state is GAME_PLAYING
        elif self.state == GAME_STATE.GAME_PLAYING:

            # todo
            # add check to only listen on button presses of active players

        
            if self.mode == GAME_MODE.GAME_1:
                self.game_1_click(number)

            elif self.mode == GAME_MODE.GAME_2:
                self.game_2_click(number)

            elif self.mode == GAME_MODE.GAME_3:
                self.game_3_click(number)

            elif self.mode == GAME_MODE.GAME_4:
                print("todo")
                # TODO
        
            elif self.mode == GAME_MODE.GAME_5:
                print("todo")
                # TODO
            
            elif self.mode == GAME_MODE.GAME_6:
                print("todo")
                # TODO
            
            elif self.mode == GAME_MODE.GAME_7:
                print("todo")
                # TODO
            
            elif self.mode == GAME_MODE.GAME_8:
                print("todo")
                # TODO



    # helper methods to handle player button presses for each different game mode

    def game_1_click(self, number):

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

        for player in self.players:
            player.clear_counter()


        # GAME 1: 
        #
        # every player is pressing his button as often as possible in 10 seconds, player wiht the highest count wins
        #
        if self.mode == GAME_MODE.GAME_1:

            for player in filter(Player.is_active, self.players):
                player.display.set_text(player.counter)

            gameThread = threading.Thread(target=self.game_1_thread, args=())
            gameThread.start()


        # GAME 2:
        #
        # todo
        #
        elif self.mode == GAME_MODE.GAME_2:

            self.timer = threading.Timer(1.0, self.game_2_over)
            self.timer.start()

            active_players = list(filter(Player.is_active, self.players))

            new_player = random.choice(active_players)
            new_player.arcade_button.switch_on()

        # GAME 3:
        #
        #
        #
        elif self.mode == GAME_MODE.GAME_3:

            print("Not yet implemented")

        # GAME 4:
        #
        #
        #
        elif self.mode == GAME_MODE.GAME_4:

            print("Not yet implemented")

        # GAME 5:
        #
        #
        #
        elif self.mode == GAME_MODE.GAME_5:

            print("Not yet implemented")

        # GAME 6:
        #
        #
        #  
        elif self.mode == GAME_MODE.GAME_6:

            print("Not yet implemented")

        # GAME 7:
        #
        #
        #
        elif self.mode == GAME_MODE.GAME_7:

            print("Not yet implemented")

        # GAME 8:
        #
        #
        #
        elif self.mode == GAME_MODE.GAME_8:

            print("Not yet implemented")



    # needed helper threads and functions for the different games

    def game_1_thread(self):

        time.sleep(10)

        active_players = list(filter(Player.is_active, self.players))

        active_players.sort(key=lambda player: player.counter, reverse=True)

        active_players[0].arcade_button.switch_on()

        print("Player ", active_players[0].get_number(), "wins!")

        self.set_game_state(GAME_STATE.GAME_OVER)


    def game_2_over(self):

        self.set_game_state(GAME_STATE.GAME_OVER)


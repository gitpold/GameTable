# imports

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


    def get_player_by_gpio(self, gpio):
        return next((x for x in self.players if x.arcade_button.button == gpio), None)

    def get_player_by_number(self, number):
        return next((x for x in self.players if x.number == number), None)


    def set_all_buttons_off(self):
        for player in self.players:
            player.arcade_button.switch_off()


    def start_game(self):

        if self.mode == 'GAME_1':
            x = threading.Thread(target=self.thread_function, args=(1,))
            x.start()


    def thread_function(self, test):
        print("thread started")
        time.sleep(10)
        self.status = 'GAME_OVER'
        print("thread ended")


    def big_button_pressed(self):

        if self.status == 'PLAYER_SELECTION':
            if len(self.get_active_players()) > 0:
                self.status = 'GAME_MODE_SELECTION'
                self.set_all_buttons_off()
                print("GAME_MODE_SELECTION")

        elif self.status == 'GAME_MODE_SELECTION':
            if self.mode != None:
                self.status = 'GAME_PLAYING'
                self.set_all_buttons_off()
                self.start_game()
                print("GAME_PLAYING")

        elif self.status == 'GAME_OVER':
            self.status == 'PLAYER_SELECTION'
            self.set_all_buttons_off()
            print("PLAYER_SELECTION")

        self.big_button.switch_off()

        # TODO

    
    def player_button_pressed(self, number):

        if self.status == 'PLAYER_SELECTION':
            self.get_player_by_number(number).toggle_active()

            if len(self.get_active_players()) > 0:
                self.big_button.switch_on()
            else:
                self.big_button.switch_off()

        elif self.status == 'GAME_MODE_SELECTION':
            if number == 1:
                self.mode = 'GAME_1'
                print(self.mode)
            else:
                self.mode = None

            if self.mode != None:
                self.big_button.switch_on()
            else:
                self.big_button.switch_off()


        elif self.status == 'GAME_PLAYING':
        
            if self.mode == 'GAME_1':
                self.game_1_click(number)

        # TODO


    def game_1_click(self, number):
        print("test " + str(number))

        player = self.get_player_by_number(number)
        player.increase_counter()
        player.display.set_text(player.counter)


    #alle LEDs an
    def switchAllLEDsOn(self):
        for button in gameTable:
            button.arcade_button.switchOn()

        for player in players:
            player.arcade_button.switchOn()

    #alle LEDs aus
    def switchAllLEDsOff(self):
        bigButton.switchOff()

        for player in players:
            player.arcade_button.switchOff()

    #LED-Animation
    def LEDAnimation(self):
        pass

    #Funktion, auf allen Displays dasselbe anzuzeigen
    def changeAllDisplays(self, text):
        seg.text = text * 8

    #Spieler zur Liste der aktiven Spieler hinzufügen
    def appendActivePlayer(self,player):
        self.activeplayers.append(player)

    #Spieler von der Liste der aktiven Speler entfernen
    def removeActivePlayer(self,player):
        self.activeplayers.remove(player)

    #Liste der aktiven Spieler clearen
    def clearActivePlayers(self):
        self.activeplayers.clear()

    #aktuellen Spielstatus ändern
    def changeStatus(self,status):
        self.status = status



    def mode1(self):
        scrollText("DAS KLAPPT LEIDER NOCH NICHT")

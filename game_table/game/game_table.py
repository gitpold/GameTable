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
        self.timer = None


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


    def clear_all(self):
        for player in self.players:
            player.arcade_button.switch_off()
            player.display.set_text('        ')


    def start_game(self):

        if self.mode == 'GAME_1':

            for player in filter(Player.is_active, self.players):
                player.clear_counter()
                player.display.set_text(player.counter)

            gameThread = threading.Thread(target=self.game_1_thread, args=(1,))
            gameThread.start()

        elif self.mode == 'GAME_2':

            for player in filter(Player.is_active, self.players):
                player.clear_counter()

            self.timer = threading.Timer(1.0, self.game_2_over)
            self.timer.start()


    def game_1_thread(self):

        time.sleep(10)

        active_players = list(filter(Player.is_active, self.players))

        active_players.sort(key=lambda player: player.counter, reverse=True)

        active_players[0].arcade_button.switch_on()


        self.status = 'GAME_OVER'



    def game_2_over(self):

        self.status = 'GAME_OVER'





    def set_game_mode_selection(self):
        self.clear_all()

        self.players[0].display.set_text('GAME 1')

        if self.mode == 'GAME_1':
            self.players[0].arcade_button.switch_on()

        print("GAME_MODE_SELECTION")

        self.status = 'GAME_MODE_SELECTION'



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
                self.players[0].arcade_button.switch_on()
                print(self.mode)
            else:
                self.players[0].arcade_button.switch_off()
                self.mode = None

            if self.mode != None:
                self.big_button.switch_on()
            else:
                self.big_button.switch_off()


        elif self.status == 'GAME_PLAYING':
        
            if self.mode == 'GAME_1':
                self.game_1_click(number)

            elif self.mode == 'GAME_2':
                self.game_2_click(number)

        # TODO


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

        active_players.remove(player)

        new_player = random.choice(active_players)

        new_player.arcade_button.switch_on()





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

# imports

import RPi.GPIO as GPIO

import time
import random

from .player import Player
from .arcade_button import ArcadeButton
from .display import Display
from .score import Score

#GameTable-Class
class GameTable(object):
    def __init__(self, players, big_button, seg):
        self.players = players
        self.big_button = big_button
        self.status = "Auswahl"


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


    def big_button_pressed(self):

        # TODO

        self.big_button.toggle()

    
    def player_button_pressed(self, number):

        # TODO

        self.get_player_by_number(number).arcade_button.toggle()


    def test2(self, players, activeplayers, bigButton, status, score, round):
        self.players = players
        self.activeplayers = activeplayers
        self.bigButton = bigButton
        self.status = status #der Status im Spiel, bspw. Modus 1, Modus 2, etc.
        self.score = score
        self.round = round

    def get_test(self):
        return "test"

    #bigButton wurde gedrückt
    def bigButtonPushed(self):
        self.big_button.switchOn()
        """ button = self
        argument = [gameTable.status, button]
        bigSwitcher(argument)
 """
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

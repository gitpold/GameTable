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

    def getPlayerByGpio(self, gpio):
        if gpio == 9:
            return 9
        else:
            return next((x for x in self.players if x.arcade_button.button == gpio), None)

    def mode1(self):
        scrollText("DAS KLAPPT LEIDER NOCH NICHT")

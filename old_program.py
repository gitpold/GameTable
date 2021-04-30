#Imports
import RPi.GPIO as GPIO
import time
import random

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

#Definition globaler Variablen
number = 0

#GPIO Setwarning/Setmode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #BCM = GPIO-Nummern

#Herstellung der Verbindung mit den Segmentanzeigen
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=8) #cascaded entspricht die Anzahl der Anzeigen
seg = sevensegment(device)
seg.text = "                                                                "
device.contrast(255)


def scrollTextHelp(text):
    global seg
    segText = text[56:64] + text[48:56] + text[40:48] + text[32:40] + text[24:32] + text[16:24] + text[8:16] + text[0:8]
    seg.text = segText

def scrollText(text):
    length = 64 - len(text)
    text = text + " " * length
    for x in range(1,50):
        time.sleep(0.2)
        #text = text[-1] + text[:-1]
        text = text[1:] + text[0]
        scrollTextHelp(text)
    seg.text = "        " * 8

#Arcade-Class
class Arcade(object):
    def __init__(self, led, button):
        self.led = led
        self.button = button
        GPIO.setup(self.led,GPIO.OUT) #Pin der LED als Output setzen
        GPIO.output(self.led,GPIO.LOW)

        GPIO.setup(button,GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin des Buttons als Input setzen

    #LED an
    def switchOn(self):
        GPIO.output(self.led,GPIO.HIGH)

    #LED aus
    def switchOff(self):
        GPIO.output(self.led,GPIO.LOW)   


#Anzeige-Class
class Anzeige(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    #Methode, um den Text des eigenen Displays zu ändern
    def changeMyDisplay(self, text):
        seg.text[self.start : self.end] = text


#GameTable-Class
class GameTable(object):
    def __init__(self, players, activeplayers, bigButton, status, score, round):
        self.players = players
        self.activeplayers = activeplayers
        self.bigButton = bigButton
        self.status = status #der Status im Spiel, bspw. Modus 1, Modus 2, etc.
        self.score = score
        self.round = round

    #bigButton wurde gedrückt
    def bigButtonPushed(self):
        button = self
        argument = [gameTable.status, button]
        bigSwitcher(argument)

    #alle LEDs an
    def switchAllLEDsOn(self):
        for button in gameTable:
            button.arcade.switchOn()

        for player in players:
            player.arcade.switchOn()

    #alle LEDs aus
    def switchAllLEDsOff(self):
        bigButton.switchOff()

        for player in players:
            player.arcade.switchOff()

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
            return next((x for x in self.players if x.arcade.button == gpio), None)

    def mode1(self):
        scrollText("DAS KLAPPT LEIDER NOCH NICHT")


#Player-Class
class Player(object):
    def __init__(self, number, arcade, anzeige, score):
        self.number = number
        self.arcade = arcade
        self.anzeige = anzeige
        self.score = score

    #wird ein Button gedrückt, passiert folgendes
    def buttonWasPushed(self, player_number): 
         
        global number
        number += 1
        print("\n", number, "x pushed")

        player = self
        argument = [gameTable.status, player]
        playerSwitcher(argument)


def playerSwitcher(argument):
    switcher = {
        "Auswahl": playerAuswahl,
        "Start": playerStart,
        "Mode 1": playerMode1
        }
    # Get the function from switcher dictionary
    func = switcher.get(argument[0], lambda: "Invalid")
    # Execute the function
    player = argument[1]
    print(func(player))

def bigSwitcher(argument):
    switcher = {
        "Auswahl": bigAuswahl,
        "Start": bigStart,
        "Mode 1": bigMode1
        }
    # Get the function from switcher dictionary
    func = switcher.get(argument[0], lambda: "Invalid")
    # Execute the function
    button = argument[1]
    print(func(button))


def playerAuswahl(x):
    # To test the value of a pin use the .input method
    channel_is_on = GPIO.input(x.arcade.led)  # Returns 0 if OFF or 1 if ON
    player_number = str(x.number)
    plnumber = player_number

    if channel_is_on:
    # Do something here
        x.arcade.switchOff()
        x.anzeige.changeMyDisplay("        ")
        gameTable.removeActivePlayer(x)
    else:
        x.arcade.switchOn()
        text2 = "PLAYER " + plnumber
        x.anzeige.changeMyDisplay(text2)
        gameTable.appendActivePlayer(x)

    print(gameTable.activeplayers)

    if len(gameTable.activeplayers) == 0:
        print("The list is empty!")
        bigButton.switchOff()
    else:
        bigButton.switchOn()
    

def bigAuswahl(x):
    if len(gameTable.activeplayers) == 0:
        print("The list is empty!")
    else:
        gameTable.switchAllLEDsOff()
        gameTable.changeAllDisplays("        ")

        time.sleep(2)

        gameTable.changeStatus("Mode 1")
        gameTable.mode1()
        print(gameTable.status)


def bigStart(x):
    pass


def playerStart(x):
    pass


def bigMode1(x):
    pass


def playerMode1(x):
    pass

            

#Score-Class
class Score(object):
    def __init__(self, points, lives):
        self.points = points
        self.lives = lives

    def ClearPoints(self):
        self.points = 0

    def IncreasePoints(self):
        self.points += 1

    def SetLives(self, lives):
        self.lives = lives
    
    def DecreaseLives(self):
        self.lives -= 1


#Button Callback
def buttonCallback(channel, player): #button entspricht der Objektnummer in der Liste und wurde bei #Button Detect übergeben
    if player == 9:
        gameTable.bigButtonPushed()
    else:
        player.buttonWasPushed(player.number) #die Funktion WasPushed für das entsprechende Objekt wird aufgerufen
    

if __name__ == '__main__':

    #Definitionen für die Klassen
    players = [
        Player(1, Arcade(12,4), Anzeige(56,64), Score(0,0)),
        Player(2, Arcade(21,14), Anzeige(48,56), Score(0,0)),
        Player(3, Arcade(16,15), Anzeige(40,48), Score(0,0)),
        Player(4, Arcade(13,23), Anzeige(32,40), Score(0,0)),
        Player(5, Arcade(6,24), Anzeige(24,32), Score(0,0)),
        Player(6, Arcade(5,22), Anzeige(16,24), Score(0,0)),
        Player(7, Arcade(26,27), Anzeige(8,16), Score(0,0)),
        Player(8, Arcade(19,17), Anzeige(0,8), Score(0,0))
        ]

    bigButton = [Arcade(20,9)]

    gameTable = GameTable(
            players,
            [], #active players
            bigButton,
            "Auswahl", #status
            "", #type of score
            0 #round
            ) #fügt die Liste der Player und die Infos über den großen Button hinzu


    for player in players:
        GPIO.add_event_detect(player.arcade.button,GPIO.FALLING,callback=lambda x: buttonCallback(x, gameTable.getPlayerByGpio(x)), bouncetime=200) #falls Button gepresst wird, wird #Button Callback aufgerufen

    for bigButton in bigButton:
        GPIO.add_event_detect(bigButton.button,GPIO.FALLING,callback=lambda x: buttonCallback(x, gameTable.getPlayerByGpio(x)), bouncetime=200) 


    message = input("Press enter to quit\n\n")
    GPIO.cleanup()

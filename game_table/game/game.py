from .game_table import GameTable
from .arcade_button import ArcadeButton
from .player import Player
from .display import Display
from .score import Score
from ..config.config import PLAYERS, BIG_BUTTON

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

import RPi.GPIO as GPIO

gameTable = None

def initialize_game():

    print("Starting game initialization...")
    
    #GPIO Setwarning/Setmode
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) #BCM = GPIO-Nummern

    # init seven segment displays
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=8) #cascaded entspricht der Anzahl der Anzeigen
    seg = sevensegment(device)
    seg.text = "                                                                "
    device.contrast(255)

    players = []

    for player in PLAYERS:
        players.append(
            Player(
                player['number'], 
                ArcadeButton(player['arcade']['led'], player['arcade']['button']), 
                Display(seg, player['display']['start'], player['display']['end']), 
                Score(0, 0)))

    big_button = ArcadeButton(BIG_BUTTON['led'], BIG_BUTTON['button'])

    global gameTable
    gameTable = GameTable(players, big_button, seg)


    for player in players:
        GPIO.add_event_detect(player.arcade_button.button, GPIO.FALLING, callback=lambda x: buttonCallback(x, gameTable.getPlayerByGpio(x)), bouncetime=200)

    print("Finished game initialization. \nReady to play!")



#Button Callback
def buttonCallback(channel, player): #button entspricht der Objektnummer in der Liste und wurde bei #Button Detect übergeben
    global gameTable

    print("test   ", player)

    gameTable.bigButtonPushed()

    if player.number == 9:
        gameTable.bigButtonPushed()
    else:
        player.buttonWasPushed(player.number) #die Funktion WasPushed für das entsprechende Objekt wird aufgerufen


def get_game_table():
    global gameTable
    return gameTable

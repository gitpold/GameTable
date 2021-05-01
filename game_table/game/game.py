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

game_table = None

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

    global game_table
    game_table = GameTable(players, big_button, seg)

    GPIO.add_event_detect(big_button.button, GPIO.FALLING, callback=big_button_callback)

    for player in players:
        GPIO.add_event_detect(player.arcade_button.button, GPIO.FALLING, callback=lambda x: player_button_callback(x, game_table.get_player_by_gpio(x)), bouncetime=200)

    print("Finished game initialization. \nReady to play!")


def big_button_callback(channel): 
    global game_table
    game_table.big_button_pressed()


#Button Callback
def player_button_callback(channel, player): #button entspricht der Objektnummer in der Liste und wurde bei #Button Detect übergeben
    global game_table
    game_table.player_button_pressed(player.get_number)


def get_game_table():
    global game_table
    return game_table

#Imports
import RPi.GPIO as GPIO

class ArcadeButton(object):
    def __init__(self, led, button):
        self.led = led
        self.button = button
        self.state = False

        GPIO.setup(self.led,GPIO.OUT) #Pin der LED als Output setzen
        GPIO.setup(button,GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin des Buttons als Input setzen

        self.set_led(False)

    def set_led(self, state):
        if state:
            GPIO.output(self.led, GPIO.HIGH)
        else:
            GPIO.output(self.led, GPIO.LOW)

    def get_all(self):
        return { 'state': self.state }

    #LED an
    def switch_on(self):
        self.set_led(True)

    #LED aus
    def switch_off(self):
        self.set_led(False)

    def toggle(self):
        self.state = not self.state
        self.set_led(self.state)

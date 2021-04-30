#Imports
import RPi.GPIO as GPIO

class ArcadeButton(object):
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

# || Reset Skript zum neustarten des Pi ||
import os, sys, time, RPi.GPIO as gpio

# GPIO Pins festlegen
gpio.setmode(gpio.BOARD)   # Pin-Nummern des P1/J8-Headers
gpio.setup(21, gpio.IN)    # Pin 21 ist mit Reset-Button verbunden


while 1:
  # Wenn der Aus-Schalter gedrückt wird, soll der sudo reboot command ausgeführt werden
  if gpio.input(21)==gpio.LOW:
    os.system("reboot")
    sys.exit()
  time.sleep(0.3)
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners.keypad import KeysScanner

# fmt: off
_KEY_CFG = [
    board.KEY1,  board.KEY2,  board.KEY3,
    board.KEY4,  board.KEY5,  board.KEY6,
    board.KEY7,  board.KEY8,  board.KEY9,
    board.KEY10, board.KEY11, board.KEY12,
]
# fmt: on


class KMKKeyboard(_KMKKeyboard):
    rgb_pixel_pin = board.NEOPIXEL
    rgb_num_pixels = 12
    encoder_pins = ((board.ENCODER_A, board.ENCODER_B, board.ENCODER_SWITCH),)
    led_pin = board.LED
    display = board.DISPLAY
    display_sleep_command = 0xAE
    display_wake_command = 0xAF

    def __init__(self):
        self.matrix = KeysScanner(pins=_KEY_CFG)

from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler as _EncoderHandler
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.extensions.display import Display, TextEntry, BuiltInDisplay
from kmk.extensions.LED import LED
from kmk.extensions.lock_status import LockStatus

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())

rgb = RGB(
    pixel_pin=keyboard.rgb_pixel_pin,
    num_pixels=keyboard.rgb_num_pixels,
    animation_mode=AnimationModes.STATIC_STANDBY,
)
keyboard.extensions.append(rgb)


def format_display_layer(
    name: str, layer: int, encoder: str, map: list[str]
) -> list[TextEntry]:
    text_map = []
    text_map.append(
        TextEntry(
            text=f'L{layer}: {name}',
            inverted=True,
            layer=layer,
        )
    )
    text_map.append(
        TextEntry(
            text=f'Enc: {encoder}',
            x=keyboard.display.width,
            x_anchor='R',
            layer=layer,
        )
    )

    x_anchors = ['L', 'M', 'R']

    for i in range(12):
        x = i % 3
        y = i // 3
        text_map.append(
            TextEntry(
                text=map[i],
                x=(keyboard.display.width - 1) * x / 2,
                y=(keyboard.display.height - 1) - (3 - y) * 12,
                x_anchor=x_anchors[x],
                y_anchor='B',
                layer=layer,
            )
        )

    return text_map


display = Display(
    display=BuiltInDisplay(
        display=keyboard.display,
        sleep_command=keyboard.sleep_command,
        wake_command=keyboard.wake_command,
    ),
    width=keyboard.display.width,
    height=keyboard.display.height,
)
keyboard.extensions.append(display)


# Replace default encoder behavior with layer switching
# If you would rather have the default behavior, simply delete this
# and remove 'as _EncoderHandler' in the imports at the top
class EncoderHandler(_EncoderHandler):
    def on_move_do(self, keyboard, encoder_id, state):
        num_layers = len(keyboard.keymap)
        current_layer = keyboard.active_layers[-1]
        new_layer = (current_layer + state['direction']) % num_layers
        keyboard.active_layers[-1] = new_layer


encoder_handler = EncoderHandler()
encoder_handler.pins = keyboard.encoder_pins
keyboard.modules.append(encoder_handler)

led = LED(led_pin=keyboard.led_pin)
keyboard.extensions.append(led)


class LEDLockStatus(LockStatus):
    def set_lock_leds(self):
        led.set_brightness(50 if self.get_num_lock() else 0, leds=[0])

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            self.set_lock_leds()


keyboard.extensions.append(LEDLockStatus())


# What appears on the display
# fmt: off
display.entries = format_display_layer(
    'Keypad',
    0,
    'Num Lk',
    [
        '7/Home', '8/^',   '9/PgUp',
        '4/<',    '5',     '6/>',
        '1/End',  '2/v',   '3/PgDn',
        './Del',  '0/Ins', 'Enter',
    ],
) + format_display_layer(
    'Mouse',
    1,
    'N/A',
    [
        'LMB',   'MMB',   'RMB',
        'BTN4',  'Up',    'BTN5',
        'Left',  'Down',  'Right',
        'AutoL', 'AutoM', 'AutoR',
    ],
)
# fmt: on

# fmt: off
keyboard.keymap = [
    [
        KC.KP_7, KC.KP_8, KC.KP_9,
        KC.KP_4, KC.KP_5, KC.KP_6,
        KC.KP_1, KC.KP_2, KC.KP_3,
        KC.PDOT, KC.KP_0, KC.PENT,
    ],
    [
        KC.MB_LMB,        KC.MB_MMB,        KC.MB_RMB,
        KC.MB_BTN4,       KC.MS_UP,         KC.MB_BTN5,
        KC.MS_LT,         KC.MS_DN,         KC.MS_RT,
        KC.RF(KC.MB_LMB), KC.RF(KC.MB_MMB), KC.RF(KC.MB_RMB),
    ],
]
# fmt: on

# Encoder button mapping
# Encoder movement mappings will be ignored anyways
encoder_button_map = [
    KC.NLCK,
    None,
]
encoder_handler.map = [((None, None, key),) for key in encoder_button_map]

if __name__ == '__main__':
    keyboard.go()

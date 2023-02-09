# menu-states
# circuitpython 8.0
import asyncio
import time
import board
import neopixel
import statemachine

import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
import adafruit_displayio_ssd1306

lastX = 0
lastY = 0
display = None
graph = None
splash = None
darkGroup = None
i2c = board.I2C()
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed

def initDisplay() :
    global lastX, lastY, graph, darkGroup, splash, display
    displayio.release_displays()
    oled_reset = board.D9

    # Use for I2C
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C, reset=oled_reset)

    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

    # Make a splash display Group
    splash = displayio.Group()
    display.show(splash)
    # Draw a label
    text = "hydrate-glide-path"
    text_area = label.Label(
        terminalio.FONT, text=text, color=0xffffff, x=20, y=HEIGHT // 2 - 1
    )
    splash.append(text_area)

    # Make a graph display Group 
    graph = displayio.Group()

    color_bitmap2 = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette2 = displayio.Palette(1)
    color_palette2[0] = 0x000000 

    bg_sprite2 = displayio.TileGrid(color_bitmap2, pixel_shader=color_palette2, x=0, y=0)
    graph.append(bg_sprite2)
    # draw a line
    # graph.append(Line(0, 0, 127, 31, 0xffffff))
    lastX = 0
    lastY = 0
    # Make the display context
    darkGroup = displayio.Group()
    bg_sprite3 = displayio.TileGrid(color_bitmap2, pixel_shader=color_palette2, x=0, y=0)
    darkGroup.append(bg_sprite3)

    bg_sprite2 = displayio.TileGrid(color_bitmap2, pixel_shader=color_palette2, x=0, y=0)


def mapRange(val, in_min, in_max, out_min, out_max) :
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def addLine(t, level):
    global lastX, lastY
    if level < bottom :
        return
    toX = int(mapRange( t, 0, duration_seconds, 0, 127))
    if not toX > lastX + 2 :
        return
    toY = int(mapRange(level, bottom, top, 31, 0))
    print(lastX, lastY, toX, toY)
    graph.append(Line(lastX, lastY, toX, toY, 0xffffff))
    lastX = toX
    lastY = toY

def displayMsg(msgs):
    global splash
    print(msgs)
    messages = len(msgs)
    while len(splash) :
        splash.pop()
    i = 1
    for m in msgs :
        text_area = label.Label(
            terminalio.FONT, text=m, color=0xffffff, x=1, y=(HEIGHT // (2 * messages) * i * 2) + ((6 - messages) * -1) - 3
        )
        splash.append(text_area)
        i += 1
    display.show(splash)
    touchTimeOut()

from digitalio import DigitalInOut, Direction, Pull


pixel_pin = board.NEOPIXEL
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)


def screen_off(t) :
    print("display off")
    display.show(darkGroup)

time_out = 0
time_out_decaseconds = 100
def touchTimeOut() :
    global time_out
    time_out = 0

def setTimeOut(decaseconds) :
    global time_out_decaseconds
    time_out_decaseconds = decaseconds

async def time_out_click():
    global time_out
    while True:
        await asyncio.sleep(0.1)
        time_out += 1
        if time_out > time_out_decaseconds:
            statemachine.enqueue("timeout")
            time_out = 0

def initAll(_state):
    initDisplay()
    statemachine.enqueue("done")
def show_status(_state):
    touchTimeOut()
    setTimeOut(100)
    displayMsg(["show_status"])
def show_state_name(state):
    touchTimeOut()
    setTimeOut(200)
    displayMsg([state["entry"]])
def blank_screen(state):
    display.show(darkGroup)
fn_map = {
    "init": initAll,
    "startup_screen": show_state_name,
    "startup_screen_2": show_state_name,
    "startup_screen_3": show_state_name,
    "show_status": show_status,
    "menu": show_state_name,
    "menu_task_c": show_state_name,
    "menu_task_c2": show_state_name,
    "menu_task_c3": show_state_name,
    "blank_screen": blank_screen
}

menu_states = {
    "id": "Hydrate-U",
    "initial": "startup",
    "states": {
        "startup": {
            "entry": "init",
            "on": {
                "done": {
                    "target": "startup screen"
                }
            }
        },
        "startup screen": {
            "entry": "startup_screen",
            "on": {
                "button_b_release": {
                    "target": "startup screen 2"
                }
            }
        },
        "startup screen 2": {
            "entry": "startup_screen_2",
            "on": {
                "button_b_release": {
                    "target": "startup screen 3"
                }
            }
        },
        "startup screen 3": {
            "entry": "startup_screen_3",
            "on": {
                "button_b_release": {
                    "target": "show status"
                }
            }
        },
        "show status": {
            "entry": "show_status",
            "on": {
                "timeout": {
                    "target": "blank screen"
                },
                "button_b_release": {
                    "target": "menu"
                },
                "long_button_b": {
                    "target": "show graph"
                },
                "long_button_a": {
                    "target": "time left"
                }
            }
        },
        "blank screen": {
            "entry": "blank_screen",
            "on": {
                "button_b_release": {
                    "target": "menu"
                },
                "button_a_release": {
                    "target": "show status"
                }
            }
        },
        "menu": {
            "entry": "menu",
            "on": {
                "button_b_release": {
                    "target": "menu task C"
                },
                "long_button_a": {
                    "target": "startup screen"
                },
                "button_a_release": {
                    "target": "show status"
                }
            }
        },
        "menu task C": {
            "entry": "menu_task_c",
            "on": {
                "button_b_release": {
                    "target": "menu task C 2"
                }
            }
        },
        "menu task C 2": {
            "entry": "menu_task_c2",
            "on": {
                "button_b_release": {
                    "target": "menu task C 3"
                }
            }
        },
        "menu task C 3": {
            "entry": "menu_task_c3",
            "on": {
                "button_b_release": {
                    "target": "show status"
                }
            }
        },
        "show graph": {
            "entry": "show_graph",
            "on": {
                "timeout": {
                    "target": "blank screen"
                },
                "button_a_release": {
                    "target": "show status"
                }
            }
        },
        "time left": {
            "entry": "time_left",
            "on": {
                "timeout": {
                    "target": "blank screen"
                },
                "button_a_release": {
                    "target": "show status"
                }
            }
        }
    }
}

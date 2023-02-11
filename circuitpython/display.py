import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

display = None
splash = None
darkGroup = None
i2c = board.I2C()
WIDTH = 128
HEIGHT = 32  # some displays are 64


def initDisplay():
    global darkGroup, splash, display
    displayio.release_displays()
    oled_reset = board.D9

    # Use for I2C
    display_bus = displayio.I2CDisplay(i2c,
                                       device_address=0x3C,
                                       reset=oled_reset)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus,
                                                 width=WIDTH,
                                                 height=HEIGHT)

    # Make a splash display Group
    splash = displayio.Group()
    display.show(splash)
    # Draw a label
    text = "menu-states"
    text_area = label.Label(terminalio.FONT,
                            text=text,
                            color=0xffffff,
                            x=20,
                            y=HEIGHT // 2 - 1)
    splash.append(text_area)

    # Make a graph display Group
    graph = displayio.Group()

    color_bitmap2 = displayio.Bitmap(WIDTH, HEIGHT, 1)
    color_palette2 = displayio.Palette(1)
    color_palette2[0] = 0x000000

    # Make the display context
    darkGroup = displayio.Group()
    bg_sprite3 = displayio.TileGrid(color_bitmap2,
                                    pixel_shader=color_palette2,
                                    x=0,
                                    y=0)
    darkGroup.append(bg_sprite3)



def displayMsg(msgs):
    global splash
    print(msgs)
    messages = len(msgs)
    while len(splash):
        splash.pop()
    i = 1
    for m in msgs:
        text_area = label.Label(terminalio.FONT,
                                text=m,
                                color=0xffffff,
                                x=1,
                                y=(HEIGHT // (2 * messages) * i * 2) +
                                ((6 - messages) * -1) - 3)
        splash.append(text_area)
        i += 1
    display.show(splash)


def screen_off():
    print("display off")
    display.show(darkGroup)


initDisplay()
display.show(darkGroup)
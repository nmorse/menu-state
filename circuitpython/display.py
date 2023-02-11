import board
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
HEIGHT = 32  # some displays are 64


def initDisplay():
    global lastX, lastY, graph, darkGroup, splash, display
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

    bg_sprite2 = displayio.TileGrid(color_bitmap2,
                                    pixel_shader=color_palette2,
                                    x=0,
                                    y=0)
    graph.append(bg_sprite2)
    # draw a line
    lastX = 0
    lastY = 0
    # Make the display context
    darkGroup = displayio.Group()
    bg_sprite3 = displayio.TileGrid(color_bitmap2,
                                    pixel_shader=color_palette2,
                                    x=0,
                                    y=0)
    darkGroup.append(bg_sprite3)

    bg_sprite2 = displayio.TileGrid(color_bitmap2,
                                    pixel_shader=color_palette2,
                                    x=0,
                                    y=0)


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


def display_graph(data):
    display.show(graph)
    while len(graph):
        graph.pop()
    previous = None
    for pts in data:
        if previous == None:
            previous = pts
        else:
            graph.append(
                Line(previous[0], previous[1], pts[0], pts[1], 0xffffff))
            previous = pts

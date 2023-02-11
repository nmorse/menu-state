# menu-states
# circuitpython 8.0
import asyncio
import statemachine
from display import initDisplay, displayMsg, display, screen_off, display_graph

time_out = 0
time_out_decaseconds = 100


def touchTimeOut():
    global time_out
    time_out = 0


def setTimeOut(decaseconds):
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
    screen_off()


def show_graph(state):
    touchTimeOut()
    setTimeOut(200)
    display_graph([[0,31],[20,12],[40,22],[60,2],[80,10],[100,27],[120,0],[127,5]])


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
    "blank_screen": blank_screen,
    "time_left": show_state_name,
    "show_graph": show_graph
}

menu_states = {
    "id": "menu_states",
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
                "button_b": {
                    "target": "startup screen 2"
                },
                "timeout": {
                    "target": "startup screen 2"
                }
            }
        },
        "startup screen 2": {
            "entry": "startup_screen_2",
            "on": {
                "button_b": {
                    "target": "startup screen 3"
                },
                "timeout": {
                    "target": "startup screen 3"
                }
            }
        },
        "startup screen 3": {
            "entry": "startup_screen_3",
            "on": {
                "button_b": {
                    "target": "show status"
                },
                "timeout": {
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
                "button_b": {
                    "target": "menu"
                },
                "button_b_long_press": {
                    "target": "show graph"
                },
                "button_a_long_press": {
                    "target": "time left"
                }
            }
        },
        "blank screen": {
            "entry": "blank_screen",
            "on": {
                "button_b": {
                    "target": "menu"
                },
                "button_a": {
                    "target": "show status"
                }
            }
        },
        "menu": {
            "entry": "menu",
            "on": {
                "button_b": {
                    "target": "menu task C"
                },
                "button_a_long_press": {
                    "target": "startup screen"
                },
                "button_a": {
                    "target": "show status"
                },
                "timeout": {
                    "target": "blank screen"
                }
            }
        },
        "menu task C": {
            "entry": "menu_task_c",
            "on": {
                "button_b": {
                    "target": "menu task C 2"
                },
                "timeout": {
                    "target": "menu task C 2"
                }
            }
        },
        "menu task C 2": {
            "entry": "menu_task_c2",
            "on": {
                "button_b": {
                    "target": "menu task C 3"
                },
                "timeout": {
                    "target": "menu task C 3"
                }
            }
        },
        "menu task C 3": {
            "entry": "menu_task_c3",
            "on": {
                "button_b": {
                    "target": "menu"
                },
                "timeout": {
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
                "button_a": {
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
                "button_a": {
                    "target": "show status"
                }
            }
        }
    }
}
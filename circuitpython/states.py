# menu-states-a
# circuitpython 8.0
import asyncio
from display import displayMsg


def show_state_name(state):
    displayMsg([state["entry"]])

fn_map = {
    "begin": show_state_name,
    "choice_1A": show_state_name,
    "choice_1B": show_state_name,
    "choice_2A": show_state_name,
    "choice_2B": show_state_name,
    "choice_2C": show_state_name,
    "choice_2D": show_state_name
}

menu_states = {
  "id": "menu_states_a",
  "initial": "begin",
  "states": {
    "choice 1A": {
      "entry": "choice_1A",
      "on": {
        "button_a": {
          "target": "choice 2A"
        },
        "button_b": {
          "target": "choice 2B"
        }
      }
    },
    "choice 1B": {
      "entry": "choice_1B",
      "on": {
        "button_a": {
          "target": "choice 2C"
        },
        "button_b": {
          "target": "choice 2D"
        }
      }
    },
    "choice 2A": {
      "entry": "choice_2A",
      "on": {
        "button_b": {
          "target": "choice 2C"
        },
        "button_a": {
          "target": "begin"
        }
      }
    },
    "choice 2B": {
      "entry": "choice_2B",
      "on": {
        "button_a": {
          "target": "choice 1B"
        },
        "button_b": {
          "target": "choice 2D"
        }
      }
    },
    "choice 2C": {
      "entry": "choice_2C",
      "on": {
        "button_a": {
          "target": "choice 2B"
        },
        "button_b": {
          "target": "choice 2A"
        }
      }
    },
    "choice 2D": {
      "entry": "choice_2D",
      "on": {
        "button_a": {
          "target": "choice 2C"
        },
        "button_b": {
          "target": "choice 1A"
        }
      }
    },
    "begin": {
      "description": "the beginning of the story",
      "entry": "begin",
      "on": {
        "button_a": {
          "target": "choice 1A"
        },
        "button_b": {
          "target": "choice 1B"
        }
      }
    }
  }
}


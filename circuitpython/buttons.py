import asyncio
import keypad
# import time
from statemachine import enqueue

async def catch_pin_transitions(pin, pressed_val, alias):
    """Sends a message when the button (on the pin) is pressed, long pressed."""
    with keypad.Keys( (pin,), value_when_pressed=pressed_val) as keys:
        down_time = -1
        long_press_centaseconds = 130
        while True:
            event = keys.events.get()
            if event:
                if event.pressed:
                    down_time = 0
                if event.released:
                    if down_time >= 0 and down_time < long_press_centaseconds:
                        enqueue(alias)
                    down_time = -1
            else :
                if down_time >= long_press_centaseconds:
                    enqueue(alias+"_long_press")
                    down_time = -1

            await asyncio.sleep(0.01)
            if down_time >= 0:
                down_time += 1

# import board
# async def main():
#     interrupt_task10 = asyncio.create_task(catch_pin_transitions(board.D10))
#     interrupt_task9 = asyncio.create_task(catch_pin_transitions(board.D9))
#     await asyncio.gather(interrupt_task10, interrupt_task9)

# asyncio.run(main())
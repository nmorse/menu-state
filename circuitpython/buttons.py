import asyncio
import keypad
import time
from statemachine import enqueue

async def catch_pin_transitions(pin, pressed, alias):
    """Sends a message when button is pressed, released."""
    with keypad.Keys( (pin,), value_when_pressed=pressed) as keys:
        down_time = 0
        while True:
            event = keys.events.get()
            if event:
                if event.pressed:
                    enqueue(alias+"_press")
                    # print("pin went low", pin)
                elif event.released:
                    enqueue(alias+"_release")
                    # print("pin went high", pin)
            await asyncio.sleep(0)

# import board
# async def main():
#     interrupt_task10 = asyncio.create_task(catch_pin_transitions(board.D10))
#     interrupt_task9 = asyncio.create_task(catch_pin_transitions(board.D9))
#     await asyncio.gather(interrupt_task10, interrupt_task9)

# asyncio.run(main())
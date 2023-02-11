import board
import asyncio
from statemachine import xstate_interpreter
from states import menu_states
from buttons import catch_pin_transitions

async def main():
    async_button_a = asyncio.create_task(catch_pin_transitions(board.A3, True, "button_a"))
    async_button_b = asyncio.create_task(catch_pin_transitions(board.D2, False, "button_b"))
    async_statemachine = asyncio.create_task(xstate_interpreter(menu_states))
    await asyncio.gather(async_button_a, 
                         async_button_b, 
                         async_statemachine, 
                         )

asyncio.run(main())
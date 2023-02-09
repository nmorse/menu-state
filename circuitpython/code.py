import board
import asyncio
from statemachine import xstate_interpreter
from states import menu_states, time_out_click
from buttons import catch_pin_transitions

async def main():
    async_button_a = asyncio.create_task(catch_pin_transitions(board.A3, True, "button_a"))
    async_button_a = asyncio.create_task(catch_pin_transitions(board.D2, False, "button_b"))
    async_statemachine = asyncio.create_task(xstate_interpreter(menu_states))
    async_time_out = asyncio.create_task(time_out_click())
    await asyncio.gather(async_button_a, 
                         async_button_a, 
                         async_statemachine, 
                         async_time_out)

asyncio.run(main())
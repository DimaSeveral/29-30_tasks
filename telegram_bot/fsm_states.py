from dataclasses import dataclass
from telegram.ext import ContextTypes
from typing import Callable, Awaitable, Dict
from handlers import *  # или импортируй явно

@dataclass(frozen=True)
class State:
    name: str
    handler: callable

# Определения состояний
MAIN_MENU = State("main_menu", main_menu_handler)
TASK1_INPUT = State("task1_input", task1_input_handler)
TASK2_INPUT = State("task2_input", task2_input_handler)
TASK4_INPUT_A = State("task4_input_a", task4_input_a_handler)
TASK4_INPUT_B = State("task4_input_b", task4_input_b_handler)   # ← ДОЛЖНО БЫТЬ ЗДЕСЬ!
TASK4_INPUT_OP = State("task4_input_op", task4_input_op_handler) # ← И ЗДЕСЬ!
SUBSCRIBE = State("subscribe", subscribe_handler)

FSM_STATES = {
    state.name: state for state in [
        MAIN_MENU,
        TASK1_INPUT,
        TASK2_INPUT,
        TASK4_INPUT_A,
        TASK4_INPUT_B,      
        TASK4_INPUT_OP,     
        SUBSCRIBE
    ]
}

# Карта состояний
FSM_STATES: Dict[str, State] = {
    state.name: state
    for state in [MAIN_MENU, TASK1_INPUT, TASK2_INPUT, TASK4_INPUT_A,
                  TASK4_INPUT_B, TASK4_INPUT_OP, SUBSCRIBE]
}

def get_current_state(context: ContextTypes.DEFAULT_TYPE) -> State:
    """Получить текущее состояние из контекста"""
    state_name = context.user_data.get("fsm_state", "main_menu")
    return FSM_STATES.get(state_name, MAIN_MENU)

def set_state(context: ContextTypes.DEFAULT_TYPE, state: State) -> None:
    """Установить новое состояние"""
    context.user_data["fsm_state"] = state.name
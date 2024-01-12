from aiogram.fsm.state import StatesGroup, State


class TriggerAddState(StatesGroup):
    choice_word = State()
    choice_answer = State()


class TriggerRemoveState(StatesGroup):
    choice_remove_word = State()

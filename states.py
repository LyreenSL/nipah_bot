from aiogram.fsm.state import StatesGroup, State


class TriggerAddState(StatesGroup):
    choice_word = State()
    choice_answer = State()


class TriggerRemoveState(StatesGroup):
    choice_remove_word = State()


class ActionAddState(StatesGroup):
    choice_interaction = State()
    choice_command = State()
    choice_text = State()


class ActionRemoveState(StatesGroup):
    choice_remove_action = State()

from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class ChooseTest(CallbackData, prefix='test'):
    test_id: str

class StartTest(CallbackData, prefix='start'):
    code: str
    test_id: str

class TestAnswer(CallbackData, prefix='answer'):
    code: str
    index: int
    letter: str

class NextQuestion(CallbackData, prefix='next'):
    code: str

class CompleteTest(CallbackData, prefix='complete'):
    code: str

class ShowResults(CallbackData, prefix='show_result'):
    id: int
    

class TestConnection(StatesGroup):
    code = State()
    name = State()
    wrong_code = State()
    
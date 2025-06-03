from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class ChooseTest(CallbackData, prefix='test'):
    test_id: str

class TestConnection(StatesGroup):
    code = State()
    name = State()
    wrong_code = State()
    
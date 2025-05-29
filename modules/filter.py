from aiogram.filters import Filter
from aiogram.types import Message
from .settings import students

# Фільтр для перевірки стану студента
class StudentStateFilter(Filter):
    def __init__(self, state: str):
        self.state = state

    async def __call__(self, message: Message):
        student_state = students.get(message.from_user.id).get('state')
        return self.state == student_state



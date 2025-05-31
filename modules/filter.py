from aiogram.filters import BaseFilter
from aiogram.types import Message
from .settings import students

# Фільтр для перевірки стану студента
class StudentStateFilter(BaseFilter):
    def __init__(self, state: str):
        self.state = state

    async def __call__(self, message: Message):
        student = students.get(message.from_user.id)
        if not student:
            return False
        student_state =  student.get('state')
        return self.state == student_state



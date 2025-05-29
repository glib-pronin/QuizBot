from aiogram.types import Message

# ID адмінів
admins = [6755869828]
# Функція для перевірки на адміна
def isAdmin(message: Message):
    return message.from_user.id in admins



from aiogram.types import Message

admins = [6755869828]

def isAdmin(message: Message):
    return message.from_user.id in admins



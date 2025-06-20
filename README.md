# QuizBot

**QuizBot** - зручний інструмент для викладачів, щоб проводити тестування знань студентів.

---
## 🚀 Особливості проєкту

- Проведення квізів викладачами для студентів у Telegram.

- Підтримка кількох тестів у форматі .json.

- Збереження результатів студентів у базу даних SQLite за допомогою SQLAlchemy.

- Перевірка прав доступу через систему адміністраторів.

- Реалізовано на сучасному фреймворку Aiogram 3.

---
## 📋 Як це працює?

1. Викладач запускає тест через бот.

2. Студенти приєднуються до тесту (вводять код підключення та своє ім'я).

3. Кожному студенту по черзі надсилаються питання з варіантами відповідей.

4. Результати зберігаються автоматично до бази даних.

---
## 📖 Команди бота

- `/start`- Стартова команда. Привітання та пояснення, що вміє бот
 
- `/showquizzes` - **(Адмін)** Показує список тестів у вигляді inline-клавіатури
  
- `/stop` -  **(Адмін)** Передчасне завершення тестів

- `/join` - Підключення студента до тесту

- `/results` - Показ усіх результатів певного студента
  
> **Примітка:** Деякі команди доступні лише адміністраторам (викладачам).

---
## 🛠 Використані технології
 - **Aiogram 3** — фреймворк для асинхронних Telegram-ботів

- **SQLAlchemy** — ORM для роботи з SQLite

- **JSON** — формат зберігання тестів

- **dotenv** — для конфігурацій бот-токена

---
## 🛡 Адміністратори

Бот має список Telegram ID викладачів (адмінів), які мають доступ до запуску тестів:

```
admins = []

def isAdmin(message: Message):
    return message.from_user.id in admin
```

---
## 📄 Приклад JSON-тесту
```
{
  "test_id": "python_basics",
  "title": "Python Basics",
  "questions": [
    {
      "question": "Що таке змінна у Python?",
      "options": ["Об'єкт", "Клас", "Метод", "Модуль"], 
      "correct_answer": "Об'єкт"
    }
  ]
}
```
> **Примітки:**
> - "test_id" — це назва файлу з тестом
> - Поле "options" можна не вказувати, якщо питання з введенням відповіді.

---
## 🧑‍💻 Розробник

- Ім’я: Гліб Пронін
- Роль: Розробник Telegram-бота для навчального тестування
- GitHub: [glib-pronin](https://github.com/)

---
## 📦 Установка та запуск

1. клонування репозиторію:
```
git clone <тут посилання>
cd quizbot
```

2. Встановлення залежностей:  
```
pip install -r requirements.txt
```

3. Налаштування .env:  
```
BOT_TOKEN=your_telegram_token_here
```

4. Запуск:  
```
python main.py
```

5. Створення таблиць:
```
python -m modules.bd.database
```

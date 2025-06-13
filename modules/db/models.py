from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
import datetime

Base = declarative_base()

# Функція, яка надає час проходження тесту без секунд та мілісекунд 
def get_time_without_seconds():
    return datetime.datetime.utcnow().replace(second=0, microsecond=0)

# Модель таблиці результатів проходження тестів
class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    test_name = Column(String)
    answers = Column(Text)
    grade = Column(String)
    end_time = Column(DateTime, default=get_time_without_seconds)
    student_name = Column(String)
    interrupted = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    student = relationship("Student", back_populates="results")

    def __repr__(self):
        return f"Result(id={self.id}, test_name='{self.test_name}', answers={self.answers}, grade={self.grade}, end_time={self.end_time}, student_name={self.student_name}, interrupted={self.interrupted}, student_id={self.student_id})"

# Модель таблиці студентів
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)

    results = relationship("Result", back_populates="student", cascade="all, delete")

    def __repr__(self):
        return f"Student(id={self.id}, telegram_id={self.telegram_id})"


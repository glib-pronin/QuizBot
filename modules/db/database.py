from .models import Base, Student, Result
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(engine)



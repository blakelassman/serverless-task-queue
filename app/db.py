from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
from app.config import DATABASE_URL

# creates SQLalchemy engine
engine = create_engine(DATABASE_URL)

# creates session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for orm models
Base = declarative_base()

# define task table
class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String, primary_key=True, index=True)
    type = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result = Column(String, nullable=True)

# initializes database
def init_db():
    Base.metadata.create_all(bind=engine)

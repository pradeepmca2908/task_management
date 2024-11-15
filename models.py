#FastAPI Implementation
#Database Models
from sqlalchemy import Column, Integer, String, DateTime, Enum, Foreignkey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

# Enum for Task Status
class TaskStatus(str, enum.Enum):
    pending = "Pending"
    in_progress = "In Progress"
    completed = "Completed"

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    task = relationship("Task", back_populates="user")

# Task Model
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(TaskStatus))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, Foreignkey("users.id"))
    
    user = relationship("User", back_populates="tasks")
    
    


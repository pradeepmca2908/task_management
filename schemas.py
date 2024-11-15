#Pydantic models
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


# Task Status Enum
class TaskStatusEnum(str, Enum):
    pending = "Pending"
    in_progress = "In Progress"
    completed = "Completed"

# Task pydantic model
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: TaskStatusEnum
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: Optional[TaskStatusEnum] = None
    due_date: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TaskInResponse(TaskBase):
    id: int
    class Config:
        orm_mode = True

# User pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class UserInResponse(BaseModel):
    id: int
    username: str
    
    class Config:
        orm_mode = True
    


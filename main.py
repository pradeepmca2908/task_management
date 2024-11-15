# FastAPI Routes
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from .models import User, Task, Base
from .schemas import UserCreate, TaskCreate, TaskUpdate, TaskInResponse
from .auth import hash_password, verify_password, create_access_token, verify_token
from .database import SessionLocal, engine

# Create FastAPI app
app = FastAPI()

# OAuth2 Password Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

# get DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration
@app.post("/register", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, details="User already registered")
    db_user = User(username=user.username, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    return db_user

# User login
@app.post("/login")
def login(form_data: OAuth2PasswordBearer, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, details="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token}

# Task Create
@app.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # verify token
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, details="Invalid token")
    db_user = db.query(User).filter(User.username == user_info["sub"]).first())
    # Create Task
    db_task = Task(title=task.title, description=task.description, due_date=task.due_date, status=task.status, created_at=task.created_at, updated_at=task.updated_at, user_id=db_user.id)
    db.add(db_task)
    db.commit()
    return db_task
    
# Update Task
@app.put("/tasks/{task_id}", response_model=TaskInResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, details="Invalid token")
    db_user = db.query(User).filter(User.username == user_info["sub"]).first())
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == db_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, details="Task not found")
    if task.title:
        db_task.title = task.title
    if task.description:
        db_task.description = task.description
    if task.due_date:
        db_task.due_date = task.due_date
    if task.status:
        db_task.status = task.status
    if task.updated_at:
        db_task.updated_at = task.updated_at
    db.commit()
    return db_task

# Fetch all task
@app.get("/tasks/", response_model=List[TaskInResponse])
def get_tasks(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, details="Invalid token")
    db_user = db.query(User).filter(User.username = user_info["sub"]).first()
    tasks = db.query(Task).filter(Task.user_id == db_user.id).all()
    return tasks

# Fetch single task
@app.get("/tasks/{task_id}", response_model=List[TaskInResponse])
def get_single_tasks(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, details="Invalid token")
    db_user = db.query(User).filter(User.username == user_info["sub"]).first())
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == db_user.id).first()
    return db_task

# Delete Task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, details="Invalid token")
    db_user = db.query(User).filter(User.username == user_info["sub"]).first())
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == db_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, details="Task not found to delete")
    db.delete(db_task)
    db.commit()
    
    return {"deatils": "Task deleted"}

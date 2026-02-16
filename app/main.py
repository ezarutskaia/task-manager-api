from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.crud import create_task, get_task, get_tasks, create_user, verify_password, get_user_by_email
from app.schemas import TaskCreate, TaskUpdate, TaskRead, UserCreate, UserLogin, UserRead
from typing import List
from app.exceptions import email_already_registered, invalid_credentials, task_not_found
from app.dependencies import get_current_user
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
import jwt

app = FastAPI(title="Task Management API", version="1.0.0")

@app.post("/tasks/", tags=["Tasks"], response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_task(db=db, title=task.title, description=task.description, completed=task.completed, user_id=current_user.id)

@app.get("/tasks/", tags=["Tasks"], response_model=List[TaskRead])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = get_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise task_not_found()
    return task


@app.patch("/tasks/{task_id}", tags=["Tasks"], response_model=TaskRead, response_model_exclude_none=True)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = get_task(db=db, task_id=task_id, user_id=current_user.id)
    if not db_task:
        raise task_not_found()

    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", tags=["Tasks"], status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = get_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise task_not_found()
    db.delete(task)
    db.commit()
    
@app.post("/register", tags=["Auth"], response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise email_already_registered()
    return create_user(db, user.username, user.email, user.password)

@app.post("/login", tags=["Auth"])
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise invalid_credentials()

    to_encode = {
        "sub": db_user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
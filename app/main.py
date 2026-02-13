from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Task
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate, TaskRead
from typing import List
from fastapi import status
from app.exceptions import task_not_found

app = FastAPI(title="Task Management API",
    version="1.0.0")

#Base.metadata.create_all(bind=engine)

@app.post("/tasks/", tags=["Tasks"], response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(
        db=db,
        title=task.title,
        description=task.description,
        completed=task.completed
    )

@app.get("/tasks/", tags=["Tasks"], response_model=List[TaskRead])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tasks(db=db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db=db, task_id=task_id)
    if not task:
        raise task_not_found()
    return task

@app.patch("/tasks/{task_id}", tags=["Tasks"], response_model=TaskRead, response_model_exclude_none=True)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = update_task(
        db=db,
        task_id=task_id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    if not updated_task:
        raise task_not_found()
    return updated_task

@app.delete("/tasks/{task_id}", tags=["Tasks"], status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task(db=db, task_id=task_id)
    if not deleted_task:
        raise task_not_found()
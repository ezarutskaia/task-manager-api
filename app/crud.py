from sqlalchemy.orm import Session
from app.models import Task

def create_task(db: Session, title: str, description: str = None, completed: bool = False):
    task = Task(title=title, description=description, completed=completed)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, title: str = None, description: str = None, completed: bool = None):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task
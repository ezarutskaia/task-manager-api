from sqlalchemy.orm import Session
from app.models import Task, User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_task(db: Session, title: str, user_id: int, description: str = None, completed: bool = False):
    task = Task(title=title, user_id=user_id, description=description, completed=completed)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

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

def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


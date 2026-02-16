from fastapi import HTTPException, status

def task_not_found():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

def invalid_credentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def email_already_registered():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already registered"
    )
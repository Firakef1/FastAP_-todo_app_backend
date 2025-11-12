from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils.token import varify_access_token

router = APIRouter()
cookie_scheme = APIKeyCookie(name="access_token")

@router.post("/", status_code = status.HTTP_201_CREATED)
def add_the_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db ), access_token: str = Depends(cookie_scheme)):
    try:

        token = access_token
        if not token:
            raise HTTPException(status_code = 401, detail="No token found")
        
        username = varify_access_token(token)

        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_todo = models.Todo(
            
            name=todo.name, 
            description=todo.description, 
            day=todo.day, 
            start_time=todo.start_time, 
            end_time=todo.end_time,
            user=user)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except:
        raise HTTPException(status_code=500, detail="There was an error creating the todo")


@router.get("/", status_code = status.HTTP_200_OK)
def get_all_todo(db: Session = Depends(get_db), access_token: str = Depends(cookie_scheme)):
    try:
        if not access_token:
            raise HTTPException(status_code=401, detail="no token found")
        
        username = varify_access_token(access_token)
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        

        todos = db.query(models.Todo).filter(models.Todo.user == user).all()
        return todos
    except:
        raise HTTPException(status_code=500, detail="There was an error fetching the todo")



@router.get("/{todo_id}", status_code = status.HTTP_200_OK)
def get_todo_by_id(todo_id: int ,db: Session = Depends(get_db), access_token: str = Depends(cookie_scheme)):
    try:
        if not access_token:
            raise HTTPException(status_code=401, detail="no token found")
        
        username = varify_access_token(access_token)
        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        

        todo = db.query(models.Todo).filter(models.Todo.user == user, models.Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="todo not found")
        
        return todo
    except:
        raise HTTPException(status_code=500, detail="There was an error fetching the todo")


@router.put("/{todo_id}")
def edit_todo(todo_id: int, updated: schemas.TodoCreate, db: Session = Depends(get_db), access_token: str = Depends(cookie_scheme)):
    try:
        if not access_token:
            raise HTTPException(status_code=401, detail="no token found")
        
        username = varify_access_token(access_token)

        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise HTTPException(status_code=404, detail="no user found")

        todo = db.query(models.Todo).filter(models.Todo.user == user, models.Todo.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="todo not found")


        todo.name = updated.name
        todo.description = updated.description
        todo.day = updated.day
        todo.start_time = updated.start_time
        todo.end_time = updated.end_time

        db.commit()
        db.refresh(todo)
        return todo
    except:
        raise HTTPException(status_code=500, detail="There was an error editing the todo")



@router.delete("/{todo_id}")
def delete_todo(todo_id: int, response: Response, db: Session = Depends(get_db), access_token:str = Depends(cookie_scheme)):
    try:
        if not access_token:
            raise HTTPException(status_code=401, detail="no token found")
        
        username = varify_access_token(access_token)

        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise HTTPException(status_code=404, detail="no user found")

        todo = db.query(models.Todo).filter(models.Todo.user == user, models.Todo.id == todo_id).first()

        if not todo:
            raise HTTPException(status_code=404, detail="todo not found")

        db.delete(todo)
        db.commit()
        return {"message": "Todo deleted successfully"}
    except:
        raise HTTPException(status_code=500, detail="There was an error deleting the todo")


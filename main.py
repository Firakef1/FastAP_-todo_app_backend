from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine
from .routers import todo, user


models.Base.metadata.create_all(bind=engine)


app = FastAPI(swagger_ui_parameters={"theme": "dark"})

app.include_router(todo.router, prefix="/api/todo", tags=["Todos"])
app.include_router(user.router, prefix="/api/user", tags=["Users"] )
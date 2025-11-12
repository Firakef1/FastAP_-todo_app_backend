from pydantic import BaseModel

class Todo(BaseModel):
    name: str
    description: str
    day: str
    start_time: str
    end_time: str



class TodoCreate(BaseModel):
    name: str
    description: str
    day: str
    start_time: str
    end_time: str


    class Config:
        Truefrom_attributes = True



class User(BaseModel):
    username: str
    email: str
    password: str


class CreateUser(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
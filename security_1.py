from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

mala=OAuth2PasswordBearer(tokenUrl="kock")

class User(BaseModel):
    username: str
    email: str|None=None
    FullName: str|None=None

def fake_user(token):
    return User(
        username=token +" Hi gym",
        email= "niaznalchity1989@example.com",
        FullName="Niaz Ahmed"
    )

async def get_current_user(token: Annotated[str, Depends(mala)]):
    user=fake_user(token)
    return user

@app.get("/items/")
async def read_user(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user
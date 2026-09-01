from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()


async  def read_query_parameters(q:str|None = None, skip:int = 0, limit:int = 10):
    return {"q":q, "skip": skip, "limit": limit}

commonsv=Annotated[dict, Depends(read_query_parameters)]


@app.get("/items/")
async def read_items(commons:commonsv):
    return commons

@app.get("/users/")
async def read_users(commons:commonsv):
    return commons
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

fake_items_db = [{"items":"foo"}, {"items":"bar"},{"items":"baz"}]

class Params:
    def __init__(self ,q:str|None=None, skip:int=0, limit:int=100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons:Annotated[Params, Depends()]):
    response={}
    if commons.q:
        response.update({"q":commons.q})

    items=fake_items_db[commons.skip:commons.skip+commons.limit]
    response.update({"items":items})

    return response

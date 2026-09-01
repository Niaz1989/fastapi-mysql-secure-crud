from fastapi  import FastAPI
from pygments.lexers import q

app=FastAPI()

from fastapi import FastAPI

app = FastAPI()

country_info = [{"name":"Dhaka"},{"country":"Bangladesh"},{"continent":"Asia"}]



@app.get("/country/")
async def get_country(skip:int=0, limit:int=4):
    return country_info[skip:skip+limit]

@app.get("/kashem/{kashem_id}")
async def read_item(kashem_id: str, q: str | None = None):
    if q:
        return {"kashem_id": kashem_id, "q": q}
    return {"kashem_id": kashem_id}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
@app.get("/users/{user_id}/items/{item_id}")
async def read_users(user_id:int, item_id:str,abul:str, q:str |None=None ,short:bool=True):
    item={"user_id":user_id, "item_id":item_id}

    if q:
      item.update({"q": q})
    if abul:
        item.update({"abul":abul})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

    return item


from fastapi import FastAPI
from pydantic import BaseModel


class Price(BaseModel):
    price:float
    name:str
    description:str|None=None
    tax:float|None=None

app=FastAPI()
@app.post("/price/{price_id}")

async def read_price(price_id:int, price:Price,q:str|None=None):
    price_dict={"price_id":price_id, **price.model_dump()}

    if price.tax is not None:
        price_with_tax=price.price+price.tax
        price_dict.update({"price_with_tax":price_with_tax})
    if q:
        price_dict.update({"q":q})
    return price_dict
from fastapi import FastAPI
from enum import Enum
app=FastAPI()

@app.get("/")
async def get_me():
    return f"hello fuck me"
food={
    "indian":["samosa","singara","hvhjvhv"],
    "italian":["pizza","pasta","kkk"],
    "mexican":["zooo","popo","ddadds"]
}
class Cuisine(str,Enum):
    indian="indian"
    italian="italian"
    mexican="mexican"
@app.get("/items/{item_id}")
async def get_item(item_id: Cuisine):
    return food.get(item_id)

discounts={
    1:"10% dicount",
    2:"20% dicount",
    3:"30% dicount",
}
class Id(int,Enum):
     coupon1=1
     coupon2=2
     coupon3=3



@app.get("/discounts/{coupon_id}")
async def get_discount(coupon_id: Id):
    return discounts.get(coupon_id.value)



@app.get("/user/me")
async def get_user_me():
    return {"user_id" :"the current user"}

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return {"user_id" :user_id}


class Name(str,Enum):
    x="Amil"
    y="Niaz"
    z="Ahmed"

@app.get("/names/{name_id}")
async def get_namses(name_id: Name):
    if name_id.value == "Amil":
        return f"name_id: {name_id.value} you have right guess"
    elif name_id.value == "Niaz":
        return f"name_id: {name_id.value} you have right guess"
    elif name_id.value == "Ahmed":
        return f"name_id: {name_id.value} you have right guess"

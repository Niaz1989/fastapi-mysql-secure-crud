from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends,Query
from sqlmodel import SQLModel, create_engine, Session, select,Field

class Hero(SQLModel, table=True):
    id: int|None= Field(default=None, primary_key=True)
    name: str= Field(index=True)
    age: int= Field(default=None,index=True)
    secret_name: str


sql_file_name="database.db"
sql_url=f"sqlite:///{sql_file_name}"
connect_args={"check_same_thread":False}

engine = create_engine(sql_url, connect_args=connect_args)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

sessionDep=Annotated[Session,Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
async def startup():
    create_tables()

@app.post("/heroes")
async def create_hero(hero: Hero,session:sessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes")
async def get_heroes(session:sessionDep,limit:Annotated[int,Query(le=100)]=100,offset:int=0):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.get("/heroes/{hero_id}")
async def get_hero(hero_id:int,session:sessionDep):
    hero=session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    return hero

@app.delete("/heroes/{hero_id}")
async def delete_hero(hero_id:int,session:sessionDep):
    hero=session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok":True}


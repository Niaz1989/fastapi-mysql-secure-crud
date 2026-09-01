from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session,Field, SQLModel, create_engine,select


class HeroBase(SQLModel):
    name:str|None=Field(default=None,index=True)
    age:int=Field(default=None,index=True)

class Hero(HeroBase, table=True):
    id: int|None=Field(default=None,primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str
class HeroUpdate(HeroBase):
    name: str|None=None
    age:int|None=None
    secret_name: str|None=None


sql_lite_file="db.database"
sql_lite_url=f"sqlite:///{sql_lite_file}"
connect_args={"check_same_thread":False}
engine = create_engine(sql_lite_url,connect_args=connect_args)

def create_table():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session
SessionDep=Annotated[Session,Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def startup():
    create_table()

@app.post("/hero", response_model=HeroPublic)
async def create_hero(hero: HeroCreate,session:SessionDep):
    db_hero=Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
@app.get("/hero", response_model=list[HeroPublic])
async def get_heros(session:SessionDep,offset:int=0,limit:Annotated[int,Query(le=100)]=100):
    heroes=session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.get("/hero/{hero_id}", response_model=HeroPublic)
async def get_hero(hero_id:int,session:SessionDep):
    hero=session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    return hero

@app.patch("/hero/{hero_id}", response_model=HeroPublic)
async def update_hero(hero_id:int,update:HeroUpdate,session:SessionDep):
    hero=session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    hero_data=update.model_dump(exclude_unset=True)
    hero.sqlmodel_update(hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete("/hero/{hero_id}")
async def delete_hero(hero_id:int,session:SessionDep):
    hero=session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok":True}
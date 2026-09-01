from fastapi import FastAPI,Depends,HTTPException,status, UploadFile, File
from pydantic import BaseModel
from  sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import os
from typing import List



oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "your_secret_key_is_secure_under_precise_testing"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()
password_hasher = PasswordHash.recommended()
DATABASE_URL="mysql+pymysql://root:root@localhost:3306/test"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserTable(Base):
    __tablename__="amil_data"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255))
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    password = Column(String(255))
    profile_pic = Column(String(255), nullable=True)
    role = Column(String(50), default="user")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class AmilRequest(BaseModel):
    name:str
    age:int
    height:float
    weight:float
    password:str
    role:str|None="user"
class AmilResponse(BaseModel):
    msg:str
    name:str
    age:int
    height:float
    weight:float

class LoginRequest(BaseModel):
    name:str
    password:str

class ProfileResponse(BaseModel):
    id:int
    name:str
    age:int
    height:float
    weight:float

class ProfileUpdateRequest(BaseModel):
    name:str|None=None
    age:int|None=None
    height:float|None=None
    weight:float|None=None

def create_access_token(data:dict):
    to_encode = data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if user_name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="invalid token")

        return{"user_name":user_name,"user_id":user_id}

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid token",
                            headers={"WWW-Authenticate": "Bearer"},)





@app.post("/amil",response_model=AmilResponse)
async def amil_1(amil:AmilRequest, db:Session=Depends(get_db)):
    hashed_password = password_hasher.hash(amil.password)
    db_user=UserTable(name=amil.name,
                      age=amil.age,
                       height=amil.height,
                      weight=amil.weight,
                      password=hashed_password,
                      role=amil.role

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg":"hey this is my message",
            "name":amil.name,
            "age":amil.age,
            "height":amil.height,
            "weight":amil.weight
           }


@app.post("/login")
async def login(login_info:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(UserTable).filter(UserTable.name==login_info.name).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


    is_passord_correct=password_hasher.verify(login_info.password,user.password)
    if not is_passord_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = create_access_token(data={"sub":user.name, "user_id":user.id})


    return {"msg":"hey this is my message",
            "user_name":user.name,
            "access_token":access_token,
            "token_type":"bearer",
            "status":"welcome to the Dashbord"}

@app.get("/profile/{user_id}", response_model=ProfileResponse)
async def profile_by_id(user_id:int,db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):

    if current_user["user_id"]!=user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you do not have permission to see this user")
    user=db.query(UserTable).filter(UserTable.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


    return user


@app.patch("/profile/{user_id}", response_model=ProfileResponse)
async def profile_update(user_id:int,
                         update:ProfileUpdateRequest,
                        db:Session=Depends(get_db),
                        current_user:dict=Depends(get_current_user)):
    if current_user["user_id"]!=user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you do not have permission to see this user")


    user=db.query(UserTable).filter(UserTable.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


    if update.name is not None:
        user.name=update.name

    if update.age is not None:
        user.age=update.age
    if update.height is not None:
        user.height=update.height
    if update.weight is not None:
        user.weight=update.weight
    db.commit()
    db.refresh(user)

    return user


@app.delete("/profile/{user_id}")
async def profile_delete(user_id:int,
                         db:Session=Depends(get_db),
                         current_user:dict=Depends(get_current_user)):

    if current_user["user_id"]!=user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you do not have permission to delete other user")


    user=db.query(UserTable).filter(UserTable.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")


    db.delete(user)
    db.commit()
    return {"msg":"Delete have been successfully done"}


UPLOAD_DIR="uploaded_images"
os.makedirs(UPLOAD_DIR,exist_ok=True)
@app.post("/upload")
async def upload(file: UploadFile = File(...),
                 db:Session=Depends(get_db),
                 current_user:dict=Depends(get_current_user)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File type is not supported")



    file_ext=os.path.splitext(file.filename)[1]
    unique_file_name=f"user{current_user['user_id']}_profile{file_ext}"
    file_path=os.path.join(UPLOAD_DIR,unique_file_name)

    with open(file_path,"wb") as buffer:
        buffer.write(await file.read())

    user=db.query(UserTable).filter(UserTable.id == current_user["user_id"]).first()

    user.profile_pic=unique_file_name
    db.commit()
    db.refresh(user)

    return {"msg":"Upload have been successfully done",
            "file_name":unique_file_name}
@app.post("/admin/all-users", response_model=List[ProfileResponse])
async def get_all_users(db:Session=Depends(get_db),
                        current_user:dict=Depends(get_current_user)):

    user=db.query(UserTable).filter(UserTable.id == current_user["user_id"]).first()

    if user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="only admin  have permission to see this user")


    all_users=db.query(UserTable).all()
    return all_users











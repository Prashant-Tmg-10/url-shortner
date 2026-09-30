from fastapi import APIRouter,Depends,status,Request
from sqlalchemy.orm import Session
from src.user.dtos import userschema,userresponse,loginschema
from src.utils.db import get_db
from src.user import controller

user_routes=APIRouter(prefix="/user", tags=["user"])

@user_routes.post("/register",response_model=userresponse,status_code=status.HTTP_201_CREATED)
def register(body:userschema,db:Session=Depends(get_db)):
    return controller.register_user(body,db)

@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login(body:loginschema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)


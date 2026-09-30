from fastapi import APIRouter,Depends,status,Request
from sqlalchemy.orm import Session
from src.url.dtos import urlcreate, urlResponse
from src.utils.db import get_db
from src.url import controller
from src.user.controller import get_current_user
from src.user.models import usermodel
from fastapi.responses import RedirectResponse

url_routes=APIRouter(prefix="/url")

@url_routes.post("/create",response_model=urlResponse,status_code=status.HTTP_201_CREATED)
def new_url(body:urlcreate,db:Session=Depends(get_db),current_user:usermodel=Depends(get_current_user),):
    return controller.create_url(body,db,current_user)

@url_routes.get("/",response_model=list[urlResponse],status_code=status.HTTP_200_OK)
def get_url(db:Session=Depends(get_db),current_user:usermodel=Depends(get_current_user)):
    return controller.get_my_urls(db,current_user)


@url_routes.get("/{short_code}")
def redirect_to_orginanl(short_code:str,db:Session=Depends(get_db)):
    url=controller.get_url_and_track_click(short_code,db)
    return RedirectResponse(url=url.original_url,status_code=status.HTTP_302_FOUND)

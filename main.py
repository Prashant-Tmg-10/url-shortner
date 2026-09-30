from fastapi import FastAPI 
from src.utils.db import Base,engine
from src.user.router import user_routes
from src.user.models import usermodel
from src.url.router import url_routes
from src.url.models import urlModel


Base.metadata.create_all(bind=engine)
app=FastAPI(title="URl SHORTNER APP")
app.include_router(user_routes)
app.include_router(url_routes)

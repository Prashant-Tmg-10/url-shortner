from sqlalchemy.orm import Session
from src.url.models import urlModel
from src.url.dtos import urlcreate
from src.utils.helpers import encode_base62
from datetime import datetime
from fastapi import HTTPException, status

def create_url(body:urlcreate, db:Session, current_user):
    new_url=urlModel(
        original_url=body.original_url,
        user_id=current_user.id,
        short_code=None

    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    new_url.short_code=encode_base62(new_url.id)
    db.commit()
    db.refresh(new_url)

    return new_url

def get_my_urls(db:Session, current_user):
    return db.query(urlModel).filter(urlModel.user_id==current_user.id).all()


def get_url_and_track_click(short_code:str, db:Session):
    url=db.query(urlModel).filter(urlModel.short_code==short_code).first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT found")

    url.click_count=url.click_count + 1
    url.last_accessed_at= datetime.utcnow()
    db.commit()

    return url
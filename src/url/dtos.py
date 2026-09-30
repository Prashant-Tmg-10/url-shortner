from pydantic import BaseModel
from datetime import datetime

class urlcreate(BaseModel):
    original_url:str

class urlResponse(BaseModel):
    id:int
    original_url:str
    short_code:str
    created_at:datetime

    class config:
        from_attributes=True
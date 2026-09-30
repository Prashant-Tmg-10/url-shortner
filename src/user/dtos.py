
from pydantic import BaseModel, EmailStr


class userschema(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class loginschema(BaseModel):
    email: EmailStr
    password: str


class userresponse(BaseModel):
    id: int
    name: str
    username: str
    email: str

    class Config:
        from_attributes = True


class tokenresponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
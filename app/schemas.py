from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

class SchemaValidator(BaseModel):
    name: str
    location: str
    published: bool = True
    ratings: int = 0

class ResponseModel(BaseModel):
    id: int
    name: str
    ratings: int
    created_at: datetime
    class Config : 
        orm_mode = True 

# user schema to validate user registration

class RegistrationValidator (BaseModel):
    id: int
    email: str
    password: str
    created_at: datetime

#user schema to validate response for user registration
class RegistrationResponseValidator (BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode=True

# user login data check schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# schema to check the datatype of access_token & token_type
class Token(BaseModel):
    acces_token: str
    token_type: str

# schema to check the data that comes with the token
class TokenData(BaseModel):
    id : Optional[str] = None
from typing import Optional, List
from urllib import response
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from random import randrange
from http import HTTPStatus
import psycopg2
from psycopg2.extras import RealDictCursor
from app import oauth2
from .. import model,schemas, database
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
        prefix="/users",
        tags=["Registration"]
)


 ## add path operator to create a new registered user
@router.post("/", response_model=schemas.RegistrationResponseValidator)
async def create_user(payload: schemas.RegistrationValidator, db:Session = Depends(database.get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    hashed_password = utils.hash(payload.password) 
    payload.password = hashed_password
    new_user = model.Registration(**payload.dict())
    db.add(new_user)
    db.commit(new_user)
    db.refresh(new_user)
    return new_user

 ## add path operator to query data from registration table based on id

@router.get("/{id}", response_model=schemas.RegistrationResponseValidator)
async def query_user(payload:schemas.RegistrationValidator, id: int, db:Session = Depends(database.get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    user_query= db.query(model.Registration).filter(model.Registration.id == id).first()
    if user_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with id: {id} you entered wasn't found")
    return user_query

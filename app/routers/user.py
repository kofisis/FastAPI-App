from typing import List, Optional
from urllib import response
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import model,schemas,database, oauth2
from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
        prefix="/posts",
        tags=["Users"]
)

@router.get("/", response_model=List[schemas.ResponseModel])
async def user_input(payload: Session = Depends(database.get_db()),get_current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):
    posts = payload.query(model.Users.owner_id == get_current_user.id).limit(limit).offset(skip).all()
    return posts


@router.post("/", response_model=schemas.ResponseModel)
async def user_input(payload: schemas.SchemaValidator, db:Session = Depends(database.get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    print(get_current_user.id)

    new_post = model.Users(owner_id=get_current_user.id ,**payload.dict())
    db.add(new_post)
    db.commit(new_post)
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.ResponseModel)
async def get_post(payload: int, db: Session = Depends(database.get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    get_by_id = db.query(model.Users).filter(model.Users.owner_id == get_current_user.id).all() 

    if not get_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {payload} was not found")
    return get_by_id


#create a path operator to delete post based on id
@router.delete("/{id}")
async def delete_post(payload: int, db:Session = Depends(database.get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(model.Users).filter(model.Users.owner_id == payload).first() 
  
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the id: {payload} you entered wasn't found")
    
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform action")

    post.delete(synchronize_session=False)
    db.commit
    
    # my_post.pop(index)
    return response(f"data has been deleted")

#create a path operator to update post based in their id
@router.put("/{id}", response_model=schemas.ResponseModel)
async def update_post(payload: schemas.SchemaValidator, id: int, db: Session = Depends(database.get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Users).filter(model.Users.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the id: {id} you entered wasn't found")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform action")
    
    post_query.update(payload.dict(),synchronize_session=False)
    db.commit()

    return post
    
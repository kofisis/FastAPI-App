from fastapi import APIRouter,Depends, HTTPException, status,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,model, utils, oauth2

router = APIRouter(
        tags=["Authentication"]
                )

@router.post("/login")
async def user_login (user_creds: OAuth2PasswordRequestForm, db: Session = Depends(database.get_db())):
        user = db.query(model.Registration).filter(model.Registration.email == user_creds.username).first()
        if not user: ##if email not found
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Wrong credentials")
        if utils.verify(user_creds.password, user.password): #if hashed request pass !== hashed pass in db
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Wrong credentials")

        acces_token = oauth2.create_access_token(data={"user_id" : user.id})
        return {acces_token: "access_token","token_type":"bearer"}

        
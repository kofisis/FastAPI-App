from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from .config import settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_key_expiration_minute

def create_access_token(data : dict):
    to_encode = data.copy()

    token_expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"expire": token_expiration})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

#function to verify access_token
def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("users_id")

        if id is None:
            raise credential_exception
        token_data = schemas.Token(id=id)
    except JWTError:
        raise credential_exception
    return token_data

#function to to auto extract id, verify if token is correct by calling above function and also 
#extract id from the path operator

oauth_scheme = OAuth2PasswordRequestForm(tokenUrl = "login") #name of path operator to extract from 

def get_current_user(token: str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                        details= f"couldn't validate credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credential_exception)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashing password function
def hash(password: str):
    return pwd_context.hash(password)

#hashing login request passwords and checking to see if they match the hashed passwords in the db

def verify(plain_password ,hashed_password ):
    return pwd_context.verify( plain_password, hashed_password)


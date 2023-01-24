from fastapi import FastAPI
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware

from database import Base,engine
from routers import user,user_registration, user_login

app = FastAPI() 


origins = ["*"],

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)



app.include_router(user.router)
app.include_router(user_registration.router)
app.include_router(user_login.router)


@app.get("/")
async def user_output():
    return {"message": "welcome to my page"}





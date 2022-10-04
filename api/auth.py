from fastapi import APIRouter
from fastapi import HTTPException, status

from api.db import (
    database, User
)
from api.schemas import LoginSchema
from api.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from passlib.hash import pbkdf2_sha256

from datetime import timedelta


router = APIRouter(
    tags=['Auth']
)

@router.post('/login/')
async def login(request: LoginSchema):
    query = User.select().where(User.c.username == request.username)
    user = await database.fetch_one(query)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    if not pbkdf2_sha256.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid passsword')
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    


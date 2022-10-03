from fastapi import APIRouter
from typing import List
from fastapi import FastAPI, HTTPException, status
from api.db import (
    metadata, database, engine, User
)
from api.schemas import LoginSchema, UserSchema, UserSchemaIn
from passlib.hash import pbkdf2_sha256
from pprint import pprint as print

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
    
    return user


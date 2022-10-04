from fastapi import APIRouter

from api.db import (
    database, User
)
from api.schemas import UserSchema, UserSchemaIn

from typing import List

from passlib.hash import pbkdf2_sha256



router = APIRouter(
    tags=['Users']
)


@router.post('/user/', response_model=UserSchema)
async def create_user(user: UserSchemaIn, ):
    
    hased_password = pbkdf2_sha256.hash(user.password)
    query = User.insert().values(username=user.username, password=hased_password)
    last_record_id = await database.execute(query)
    
    return {**user.dict(), 'id': last_record_id}


@router.get('/user/', response_model=List[UserSchema])
async def get_user():
    query = User.select()
    return await database.fetch_all(query)

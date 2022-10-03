from typing import List
from fastapi import FastAPI
from api.db import (
    metadata, database, engine, Post
)
from api.schemas import PostSchema


metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startapp():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    


@app.post('/post/')
async def create_post(post: PostSchema, ):
    query = Post.insert().values(title=post.title, description=post.description)
    last_record_id = await database.execute(query)
    
    return {**post.dict(), 'id': last_record_id}


@app.get('/post/', response_model = List[PostSchema])
async def get_post():
    query = Post.select()
    return await database.fetch_all(query)




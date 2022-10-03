from typing import List
from fastapi import FastAPI, HTTPException, status
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


@app.get('/post/{id}/', response_model=PostSchema)
async def retrive_post(id: int):
    query = Post.select().where(id == Post.c.id)
    post = await database.fetch_one(query=query)
    
    if not post:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {**post}


@app.put('/post/{id}/', response_model=PostSchema)
async def put_post(id: int, post: PostSchema):
    query = Post.update().where(id == Post.c.id).values(
        title=post.title, description=post.description
        )
    await database.execute(query)
    return {**post.dict(), "id": id}


@app.delete('/post/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    query = Post.delete().where(id == Post.c.id)
    await database.execute(query)
    return {"messages": "Post deleted"}


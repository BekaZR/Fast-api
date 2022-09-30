from fastapi import FastAPI
from api.db import (
    metadata, database, engine
)

metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startapp():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    


@app.get('/post/')
async def get_post():
    return {"messages": "all post"}


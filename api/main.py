from fastapi import FastAPI

from api.db import (
    metadata, database, engine
)
from api import post, user, auth


metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startapp():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



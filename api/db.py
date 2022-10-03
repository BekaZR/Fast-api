from sqlalchemy import (
    Column, Integer, String, MetaData, 
    Table, create_engine
)

from databases import Database

DATABASE_URL = "postgresql://user:1234@localhost/fast_api"

engine = create_engine(DATABASE_URL)

metadata = MetaData()


Post = Table(
    "post",
    metadata,
    Column(
        "id", Integer, primary_key=True,
    ),
    Column(
        "title", String(60), 
    ),
    Column(
        "description", String(60), 
    ),
    
)

database = Database(DATABASE_URL)


from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str
    description: str
    



class UserSchemaIn(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    username: str

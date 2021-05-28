from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    name: str
    email: str
    writen_blog: List[Blog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str 
    body: str
    writen_by: ShowUser
    class Config():
        orm_mode = True

class ShowAllBlog(BaseModel):
    id: int
    title: str 
    body: str
    writen_by: ShowUser
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str 
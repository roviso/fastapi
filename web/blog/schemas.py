from typing import List
from pydantic import BaseModel
from typing import Optional

class recommender(BaseModel):
    id: int 
    class Config():
        orm_mode = True



#---------------BaseModel model---------------------------#
class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

#---------------User model---------------------------#
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

#---------------block model---------------------------#
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


#---------------login model---------------------------#
class Login(BaseModel):
    username: str
    password: str 


#---------------Token model---------------------------#
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
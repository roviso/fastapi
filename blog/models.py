from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key =True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("Users.id"))
    writen_by = relationship("User", back_populates = "writen_blog")

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key =True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    writen_blog = relationship("Blog", back_populates = "writen_by")
from sqlalchemy.orm import Session
from fastapi import status, HTTPException,Response
from blog import models ,schemas
from blog.hashing import Hash 

def show_all_user(db: Session):
    blogs = db.query(models.User).all()
    return blogs

def show_user(id ,db : Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND,
                            detail = f"User with id  {id} is not found")
    return user

def create_user(request: schemas.User,db : Session , status_code = status.HTTP_201_CREATED):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
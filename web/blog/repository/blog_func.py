from sqlalchemy.orm import Session
from fastapi import status, HTTPException,Response
from blog import models ,schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db : Session ):
    # return {'title':request.title, "body":request.body}
    new_blog = models.Blog(title= request.title, body = request.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Blog with id {id} is not found :( please try again!!")
    
    blog.delete(synchronize_session = False)

    db.commit()

    return "Successfully deleted"


def update(id:int, request: schemas.Blog, db:Session ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Blog with id {id} is not found :( please try again!!")
    blog.update(request)
    db.commit()
    return request

def show(id ,db : Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND,
                            detail = f"blog with id  {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"blog with id : {id} is not found"}
    return blog

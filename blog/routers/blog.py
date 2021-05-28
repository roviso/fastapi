from typing import List 
from fastapi import APIRouter, Depends, status,Response, HTTPException
from .. import schemas, models, database 
from sqlalchemy.orm import Session
from ..repository import blog_func

router = APIRouter(
    prefix = "/blog",
    tags=['Blogs']
)

@router.get('/', response_model = List[schemas.ShowAllBlog], )
def all(db: Session = Depends(database.get_db)):
    return blog_func.get_all(db)


@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(database.get_db)):
    return blog_func.create(request, db)


@router.get('/{id}', status_code = 200, response_model = schemas.ShowBlog)
def show(id,response: Response ,db : Session = Depends(database.get_db)):
    return blog_func.show(id, db)

@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(database.get_db)):
    return blog_func.destroy(id, db)

@router.put('/{id}', status_code= status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session = Depends(database.get_db)):
    return blog_func.update(id,request, db)

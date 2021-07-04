from typing import List 
from fastapi import APIRouter, Depends, status,Response, HTTPException
from blog import schemas, models, database 
from sqlalchemy.orm import Session

from blog.repository import user_func



router = APIRouter(
    prefix = "/user",
     tags=['Users']
)

@router.post('/')
def create_user(request: schemas.User,db : Session = Depends(database.get_db)):
    return user_func.create_user(request,db)

@router.get('/', response_model = List[schemas.ShowUser])
def all(db: Session = Depends(database.get_db)):
    return user_func.show_all_user(db)

@router.get('/{id}', status_code = 200, response_model = schemas.ShowUser)
def get_user(id,db : Session = Depends(database.get_db)):
    return user_func.show_user(id,db)
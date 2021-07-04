from fastapi import FastAPI, Depends, status,Response, HTTPException
from blog import models
from blog.database import engine
from blog.routers import blog, user, authentication, recommender

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.router)

app.include_router(blog.router)

app.include_router(user.router)

app.include_router(recommender.router)



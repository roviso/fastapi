from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about/{id}")
def about(id: str):
    return {"content":{"about":id}}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/list")
def show_list(limit: int=10,published : bool=True, sort:Optional[bool] = False):
    if published and limit >= 10:
        return {"message":f'{limit} published list will be shown',
                "sort": sort}
    else:
        return {"message":f'{limit} not-published list will be shown',
                "sort": sort}


class Blog(BaseModel):
    title: str
    body: str
    puiblished: Optional[bool]

@app.post("/blog")
def create_blog(request: Blog):
    return {"title": f"the title is: {request.title}",
            "body": f"body says {request.body} ans published is {request.puiblished}"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
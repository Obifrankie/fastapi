from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [{"title": "Something something", "content": "Something something something", "id": 1},
           {"title": "Something something", "content": "Something something something", "id": 2}]


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


@app.get("/posts")
async def root():
    return {"message": my_post}


"""
@app.get("/log")
def test():
    return {"data": "Welcome to my api"}

@app.post("/new")
def create(payload: dict = Body(...)):
    print(payload)
    return {"post": f"title: {payload['title']}, content: {payload['content']}"}
"""


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_post.append(post_dict)
    print(post)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"post_detail": post}

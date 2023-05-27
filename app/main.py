from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def find_post_index(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_post.append(post_dict)
    print(post)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        """
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"post {id} not found"}
        """
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"message": f"post was deleted successfully"}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"data": post_dict}

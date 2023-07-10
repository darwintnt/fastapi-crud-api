from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Text, Optional
from uuid import uuid4 as uuid


app = FastAPI()


# Post Model
class Post(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    context: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime] = None
    is_published: bool = False


posts = []


@app.get("/")
def index():
    return {"hello": "World"}


@app.get("/posts")
def get_posts():
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return {"data": post}

    raise HTTPException(404, "Post not found_")


@app.post("/posts")
def create_post(post: Post):
    post.id = str(uuid())
    posts.append(post.model_dump())
    return {"data": posts[-1]}


@app.put("/posts/{post_id}")
def update_post(post_id: str, updated_post: Post):
    for idx, post in enumerate(posts):
        if post["id"] == post_id:
            stored_item_data = posts[idx]
            stored_item_model = Post(**stored_item_data)
            update_data = updated_post.model_dump(exclude_unset=True)
            updated_item = stored_item_model.model_copy(update=update_data)
            posts[idx] = jsonable_encoder(updated_item)

            return {"data": updated_item, "message": "post updated"}

    raise HTTPException(404, "Post not found")


@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for idx, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(idx)
            return {"message": "post removed"}

    raise HTTPException(404, "Post not found")

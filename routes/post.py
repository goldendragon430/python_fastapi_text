from fastapi import APIRouter, Request
from config.dbconnection import conn
from models.post import posts
from schemas.post import Post
from typing import Any, List
from cachetools import cached
from cachetools import TTLCache

post = APIRouter()


@post.post("/addPost", tags=["posts"], response_model=Any, description="Create a post")
async def create_user(request: Request):
    try:
        post_data = await request.json()
        new_post = {}
        new_post["user_id"] = request.state.user_id
        new_post["text"] = post_data["text"]
        result = conn.execute(posts.insert().values(new_post))
        conn.commit()
        new_ele = conn.execute(
            posts.select().where(posts.c.id == result.lastrowid)
        ).first()
        return {"result": "success", "error": "", "id": new_ele[0]}
    except Exception as e:
        return {"result": "failed", "error": "Server Error", "id": -1}


@post.post(
    "/getPost",
    tags=["posts"],
    response_model=List[Post],
    description="Get a list of all posts",
)
@cached(cache=TTLCache(maxsize=10, ttl=300))  # cache feature
def get_posts(request: Request):
    try:
        user_id = request.state.user_id
        rows = conn.execute(posts.select().where(posts.c.user_id == user_id)).fetchall()
        result = []
        for row in rows:
            result.append(Post(id=row[0], text=row[1], user_id=row[2]))
        return result
    except:
        return []


@post.post(
    "/deletePost", tags=["posts"], response_model=Any, description="Delete a post"
)
async def delete_posts(request: Request):
    try:
        post_data = await request.json()
        conn.execute(posts.delete().where(posts.c.id == post_data["id"]))
        conn.commit()
        return {
            "success": True,
        }
    except:
        return {"success": False}

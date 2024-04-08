from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.user import user
from routes.post import post
from config.dbconnection import conn
from models.user import users
import uvicorn

app = FastAPI(
    title="Users API", description="a REST API using python and mysql", version="0.0.1"
)


@app.middleware("http")
async def auth(request: Request, call_next):
    url = request.url.__str__()
    # requester should append access token in header
    token = request.headers.get("token")
    # Apply Middleware for post router
    if "login" not in url and "register" not in url:
        selected_user = conn.execute(
            users.select().where(users.c.token == token)
        ).first()
        if selected_user == None:
            return JSONResponse(
                content={"error": "Invalid user", "success": False}, status_code=401
            )
        else:
            # append user_id into request body for post request
            user_id = selected_user[0]
            request.state.user_id = user_id
    response = await call_next(request)
    return response


app.include_router(user)
app.include_router(post)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

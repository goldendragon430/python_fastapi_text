from fastapi import APIRouter
from config.dbconnection import conn
from models.user import users
from schemas.user import User
from typing import Any
import cryptocode

user = APIRouter()
key = "Testing"


@user.post(
    "/register", tags=["users"], response_model=Any, description="Create a new user"
)
def create_user(user: User):
    try:
        new_user = {"name": user.name, "email": user.email}
        new_user["password"] = cryptocode.encrypt(user.password, key)
        new_user["token"] = cryptocode.encrypt(user.name, key)
        # Check if user exist with same email
        is_exist = conn.execute(
            users.select().where(users.c.email == user.email)
        ).first()
        if is_exist == None:
            conn.execute(users.insert().values(new_user))
            conn.commit()
            return {"token": new_user["token"], "result": True}
        else:
            return {"token": "", "result": False}
    except:
        return {"token": "", "result": False}


@user.post("/login", tags=["users"], response_model=Any, description="User Login")
def login(user: User):
    try:
        selected_user = conn.execute(
            users.select().where(users.c.email == user.email)
        ).first()
        if selected_user == None:
            return {"token": "", "error": "Not Exist", "result": False}
        else:

            password = cryptocode.decrypt(selected_user[3], key)
            if password == user.password:
                return {"token": selected_user[4], "error": "", "result": True}
            else:
                return {"token": "", "error": "password is wrong", "result": False}
    except:
        return {"token": "", "error": "Server Error", "result": False}

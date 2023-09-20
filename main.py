from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import HTMLResponse
import bcrypt
from db import uri
from models import User


app = FastAPI()


html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI</title>
    </head>
    <body>
        <ul>
            <li><a href="/docs">/docs</a></li>
            <li><a href="/redoc">/redoc</a></li>
        </ul>

    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

MONGO_URI = uri
client = AsyncIOMotorClient(MONGO_URI)
db = client["chatApp"]
users_collection = db["users"]


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

@app.post("/register/")
async def register_user(user: User):
    existing_username = await users_collection.find_one({"username": user.username})
    existing_email = await users_collection.find_one({"email":user.email})
    
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is registered")

    hashed_password = hash_password(user.password)

    await users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "email": user.email
    })

    return {"message": "User registered successfully"}


@app.post("/login/")
async def login(user: User):
    stored_user = await users_collection.find_one({"username": user.username})
    
    if stored_user:
        if bcrypt.checkpw(user.password.encode('utf-8'), stored_user["password"].encode('utf-8')):
            return {"message": "Login successful"}
    
    raise HTTPException(status_code=401, detail="Login failed")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from libs.events.kafka.producer import KafkaProducer
import jwt
import os

app = FastAPI()
producer = KafkaProducer(os.getenv("KAFKA_BOOTSTRAP_SERVERS"))

class User(BaseModel):
 tenantId: str
 email: str
 password: str
 profile: dict = {}

@app.post("/register")
async def register(user: User):
 # Save to database with tenantId
 await producer.publish("users", f'{{"event": "UserCreated", "tenantId": "{user.tenantId}", "email": "{user.email}"}}')
 return {"status": "registered"}

@app.post("/login")
async def login(user: User):
 token = jwt.encode({"tenantId": user.tenantId, "email": user.email}, "secret", algorithm="HS256")
 await producer.publish("users", f'{{"event": "UserLoggedIn", "tenantId": "{user.tenantId}", "email": "{user.email}"}}')
 return {"token": token}

@app.post("/logout")
async def logout():
 return {"status": "logged out"}

@app.post("/password/recover")
async def recover_password(email: str):
 await producer.publish("users", f'{{"event": "PasswordRecoveryRequested", "email": "{email}"}}')
 return {"status": "recovery email sent"}

@app.post("/password/change")
async def change_password(email: str, new_password: str):
 await producer.publish("users", f'{{"event": "PasswordChanged", "email": "{email}"}}')
 return {"status": "password changed"}

@app.get("/profile")
async def get_profile():
 return {"tenantId": "example", "email": "user@example.com", "profile": {"name": "Example User"}}

@app.get("/health")
async def health():
 return {"status": "healthy"}

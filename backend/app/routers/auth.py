import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(credentials: LoginRequest):
    token_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "username": credentials.username,
        "password": credentials.password,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return response.json()
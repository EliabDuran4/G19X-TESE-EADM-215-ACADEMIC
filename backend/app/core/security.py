import httpx
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"
)

_jwks_cache = None


async def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            _jwks_cache = response.json()
    return _jwks_cache


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
    )
    try:
        jwks = await get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
        if not rsa_key:
            raise credentials_exception
        payload = jwt.decode(token, rsa_key, algorithms=["RS256"], audience="account", options={"verify_aud": False})
        return {
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
            "roles": payload.get("realm_access", {}).get("roles", []),
        }
    except JWTError as e:
        print("JWTError:", repr(e))
        raise credentials_exception
    except Exception as e:
        print("Error validando token:", repr(e))
        raise credentials_exception


def require_role(role: str):
    async def role_checker(user: dict = Depends(get_current_user)):
        if role not in user.get("roles", []):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Se requiere el rol '{role}'")
        return user
    return role_checker
import os
from fastapi.security import HTTPBearer
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
from fastapi.security import OAuth2

#####
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from jose import jwt as jose_jwt, JWTError
# import requests
# from fastapi import Depends,HTTPException, Request, status
# from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
# from fastapi.security import OAuth2
#####


# from auth.auth import verify_token
from recipes.routes.recipes import router as recipe_router
from difficulty.routes.difficulties import router as difficulty_router
from cuisine.routes.cuisines import router as cuisine_router
from filter.routes.filter import router as filter_router
from auth.routes.auth import auth_router


app = FastAPI(title='RecipeFinder API')

origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")



# KEYCLOAK_SERVER_URL = "http://localhost:8080"
# KEYCLOAK_REALM = "test-realm"
# KEYCLOAK_CLIENT_ID = "mafatest"
# KEYCLOAK_CLIENT_SECRET = "8h0VvZ6WNkhIU1TtUwhknKtZUon31pMB"

# security = HTTPBearer()

# oauth2_scheme = OAuth2(
#     flows=OAuthFlows(
#         implicit=OAuthFlowImplicit(
#             authorizationUrl="http://localhost:8080/realms/fastapi-realm/protocol/openid-connect/auth",
#         )
#     ),
#     description="Keycloak OAuth2"
# )


# def get_public_key():
#     try:
#         url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
#         print(f"[DEBUG] Getting public key from: {url}")
#         response = requests.get(url, timeout=10)
#         print(f"[DEBUG] Public key response status: {response.status_code}")
#         if response.status_code != 200:
#             print(f"[DEBUG] Public key response: {response.text}")
#             raise Exception(f"Failed to get public key: {response.status_code}")
        
#         public_key = response.json()["public_key"]
#         full_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
#         print(f"[DEBUG] Public key retrieved successfully")
#         return full_key
#     except Exception as e:
#         print(f"[ERROR] Failed to get public key: {e}")
#         raise

# def verify_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = None
    
#     # Получение токена
#     auth_header = request.headers.get('Authorization')
#     if auth_header and auth_header.startswith('Bearer '):
#         token = auth_header[7:]
#         print(f"[DEBUG] Token from header, length: {len(token) if token else 0}")
#     else:
#         token = request.cookies.get('access_token')
#         print(f"[DEBUG] Token from cookie, length: {len(token) if token else 0}")
    
#     if not token:
#         print("[DEBUG] No token found")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="No token provided"
#         )
    
#     print(f"[DEBUG] Token first 50 chars: {token[:50] if token else None}")
    
#     try:
#         # Сначала декодируем без верификации для отладки
#         unverified_payload = jose_jwt.get_unverified_claims(token)
#         print(f"[DEBUG] Token payload: {unverified_payload}")
#         print(f"[DEBUG] Token issuer: {unverified_payload.get('iss')}")
#         print(f"[DEBUG] Token audience: {unverified_payload.get('aud')}")
#         print(f"[DEBUG] Token exp: {unverified_payload.get('exp')}")
        
#     except Exception as e:
#         print(f"[ERROR] Cannot decode token payload: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Cannot decode token: {e}"
#         )
    
#     # Получаем публичный ключ
#     try:
#         public_key = get_public_key()
#         print(f"[DEBUG] Public key retrieved, length: {len(public_key)}")
#     except Exception as e:
#         print(f"[ERROR] Failed to get public key: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Server configuration error: {e}"
#         )
    
#     # Параметры верификации
#     expected_issuer = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
#     expected_audience = KEYCLOAK_CLIENT_ID
    
#     print(f"[DEBUG] Expected issuer: {expected_issuer}")
#     print(f"[DEBUG] Expected audience: {expected_audience}")
    
#     try:
#         print("[DEBUG] Starting token verification...")
#         payload = jose_jwt.decode(
#             token,
#             public_key,
#             algorithms=["RS256"],
#             # audience=expected_audience,
#             issuer=expected_issuer,
#             options={'verify_aud': False}
#         )
#         print("[DEBUG] Token verified successfully!")
#         return payload
#     except JWTError as e:
#         print(f"[ERROR] JWT verification failed: {e}")
#         print(f"[ERROR] Token type: {type(e)}")
#         print(f"[ERROR] Error args: {e.args}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Invalid token: {str(e)}",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except Exception as e:
#         print(f"[ERROR] Unexpected error during verification: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Verification error: {str(e)}"
#         )














# def get_keycloak_public_key():
#     url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
#     response = requests.get(f"{url}/.well-known/openid-configuration")
#     jwks_uri = response.json()["jwks_uri"]
#     jwks = requests.get(jwks_uri).json()
#     return jwks


# def get_public_key():
#     url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
#     response = requests.get(url)
#     public_key = response.json()["public_key"]
#     return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"


# security = HTTPBearer()


# def verify_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = None
    
    
#     auth_header = request.headers.get('Authorization')
#     if auth_header and auth_header.startswith('Bearer '):
#         token = auth_header[7:] 
#     else:
#         # Попытка 2: Из cookie
#         token = request.cookies.get('access_token')
    
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="No token provided"
#         )
    
#     public_key = get_public_key()
    
#     try:
#         payload = jwt.decode(
#             token,
#             public_key,
#             algorithms=["RS256"],
#             audience=KEYCLOAK_CLIENT_ID,
#             issuer=f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
#         )
#         return payload
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )









# def verify_token(request: Request):
#     token = None
    
#     # Сначала пробуем получить токен из заголовка Authorization
#     try:
#         credentials = security(request)
#         token = credentials.credentials
#     except HTTPException:
#         # Если нет в заголовке, пробуем из cookie
#         token = request.cookies.get('access_token')
    
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="No token provided"
#         )
    
#     public_key = get_public_key()
    
#     try:
#         payload = jwt.decode(
#             token,
#             public_key,
#             algorithms=["RS256"],
#             audience=KEYCLOAK_CLIENT_ID,
#             issuer=f"{KEYCLOAK_SERVER_URL}realms/{KEYCLOAK_REALM}"
#         )
#         return payload
#     except JWTError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     public_key = get_public_key()
    
#     try:
#         payload = jwt.decode(
#             token,
#             public_key,
#             algorithms=["RS256"],
#             audience=KEYCLOAK_CLIENT_ID,
#             issuer=f"{KEYCLOAK_SERVER_URL}realms/{KEYCLOAK_REALM}"
#         )
#         return payload
#     except JWTError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
        # )


# @app.get("/debug/cookie")
# def debug_cookie(request: Request):
#     token = request.cookies.get('access_token')
#     return {
#         "token_exists": token is not None,
#         "token_length": len(token) if token else 0,
#         "full_token": token[:50] + "..." if token else None
#     }

# @app.get("/debug/headers")
# def debug_headers(request: Request):
#     return {
#         "headers": dict(request.headers),
#         "cookies": dict(request.cookies)
#     }




# @app.get("/api/protected")
# def protected_route(user: dict = Depends(verify_token)):
#     return {"message": "This is a protected route", "user": user}


# @app.get("/api/public")
# def public_route():
#     return {"message": "This is a public route"}


app.add_middleware(
    CORSMiddleware,
    allow_origins='http://localhost:5173',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)   


app.include_router(recipe_router)
app.include_router(difficulty_router)
app.include_router(cuisine_router)
app.include_router(filter_router)
# app.include_router(keycloak.router)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

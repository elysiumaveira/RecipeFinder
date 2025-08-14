from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt as jose_jwt, JWTError
import requests
from fastapi import Depends,HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
from fastapi.security import OAuth2


KEYCLOAK_SERVER_URL = "http://localhost:8080"
KEYCLOAK_REALM = "test-realm"
KEYCLOAK_CLIENT_ID = "mafatest"
KEYCLOAK_CLIENT_SECRET = "8h0VvZ6WNkhIU1TtUwhknKtZUon31pMB"

security = HTTPBearer()

oauth2_scheme = OAuth2(
    flows=OAuthFlows(
        implicit=OAuthFlowImplicit(
            authorizationUrl="http://localhost:8080/realms/fastapi-realm/protocol/openid-connect/auth",
        )
    ),
    description="Keycloak OAuth2"
)


def get_public_key():
    try:
        url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
        print(f"[DEBUG] Getting public key from: {url}")
        response = requests.get(url, timeout=10)
        print(f"[DEBUG] Public key response status: {response.status_code}")
        if response.status_code != 200:
            print(f"[DEBUG] Public key response: {response.text}")
            raise Exception(f"Failed to get public key: {response.status_code}")
        
        public_key = response.json()["public_key"]
        full_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
        print(f"[DEBUG] Public key retrieved successfully")
        return full_key
    except Exception as e:
        print(f"[ERROR] Failed to get public key: {e}")
        raise

# , credentials: HTTPAuthorizationCredentials = Depends(security)
def verify_token(request: Request):    
    auth_header = request.headers.get('Authorization')
    token = None
    
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header[7:]
        print(f"[DEBUG] Token from header, length: {len(token) if token else 0}")
    else:
        token = request.cookies.get('access_token')
        print(f"[DEBUG] Token from cookie, length: {len(token) if token else 0}")
    
    if not token:
        print("[DEBUG] No token found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided"
        )
    
    try:
        # Сначала декодируем без верификации для отладки
        unverified_payload = jose_jwt.get_unverified_claims(token)
        print(f"[DEBUG] Token payload: {unverified_payload}")
        print(f"[DEBUG] Token issuer: {unverified_payload.get('iss')}")
        print(f"[DEBUG] Token audience: {unverified_payload.get('aud')}")
        print(f"[DEBUG] Token exp: {unverified_payload.get('exp')}")
        
    except Exception as e:
        print(f"[ERROR] Cannot decode token payload: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Cannot decode token: {e}"
        )
    
    # Получаем публичный ключ
    try:
        public_key = get_public_key()
    except Exception as e:
        print(f"[ERROR] Failed to get public key: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server configuration error: {e}"
        )
    
    # Параметры верификации
    expected_issuer = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}"
    expected_audience = KEYCLOAK_CLIENT_ID
    
    print(f"[DEBUG] Expected issuer: {expected_issuer}")
    print(f"[DEBUG] Expected audience: {expected_audience}")
    
    try:
        print("[DEBUG] Starting token verification...")
        payload = jose_jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            # audience=expected_audience,
            issuer=expected_issuer,
            options={'verify_aud': False}
        )
        print("[DEBUG] Token verified successfully!")
        return payload
    except JWTError as e:
        print(f"[ERROR] JWT verification failed: {e}")
        print(f"[ERROR] Token type: {type(e)}")
        print(f"[ERROR] Error args: {e.args}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"[ERROR] Unexpected error during verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification error: {str(e)}"
        )
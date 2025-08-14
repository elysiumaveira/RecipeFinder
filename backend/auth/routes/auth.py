from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import httpx
from fastapi import APIRouter, HTTPException

from auth.token import verify_token



auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])

keycloak_url = 'http://localhost:8080'
realm='test-realm'
client_id='mafatest'
client_secret='8h0VvZ6WNkhIU1TtUwhknKtZUon31pMB'
redirect_url='http://localhost:8000/auth/callback'
call_back_url = 'http://localhost:5173'


@auth_router.get('/login')
async def login():
    auth_url = (
        f"{keycloak_url}/realms/{realm}/protocol/openid-connect/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={redirect_url}&"
        f"scope=openid profile email&"
        f'audience={client_id}'
    )
    print(f"Redirecting to: {auth_url}")
    return RedirectResponse(url=auth_url)
    # return {'url': auth_url, 'status': 'success'}


@auth_router.get('/callback')
async def callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        # RedirectResponse(url='/')
        return RedirectResponse(url=call_back_url)
        
    token_url = f'{keycloak_url}/realms/{realm}/protocol/openid-connect/token'
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        
    if response.status_code != 200:
        return {'error': 'Ошибка аутентификации'}
    
    tokens = response.json()
    print(f"[DEBUG] Setting cookie for tokens: {tokens.get('access_token', '')[:30] if tokens.get('access_token') else 'NONE'}")
    
    # redirect = RedirectResponse(url='/', status_code=303)
    redirect = RedirectResponse(url=call_back_url, status_code=303)
    redirect.set_cookie(
        key='access_token',
        value=tokens['access_token'],
        httponly=True,
        secure=False,
        samesite=None,
        max_age=3600
    )
    
    return redirect


@auth_router.get('/logout')
async def logout():
    logout_url = (
        f"{keycloak_url}/realms/{realm}/protocol/openid-connect/logout?"
        f"client_id={client_id}&"
        f"post_logout_redirect_uri={redirect_url}"
    )

    response = RedirectResponse(url=logout_url)
    response.delete_cookie('access_token')
    return response


@auth_router.get('/get-swagger-token')
async def get_swagger_token():
    token_url = f'{keycloak_url}/realms/{realm}/protocol/openid-connect/token'
    
    data = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': 'user', 
        'password': 'test_user',
        'scope': 'openid profile email'
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        return {
            "access_token": tokens["access_token"],
            "token_type": tokens["token_type"],
            "expires_in": tokens["expires_in"],
            "instructions": "Скопируйте значение access_token и вставьте в Swagger: Bearer ваш_токен"
        }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to get token: {response.text}"
        )


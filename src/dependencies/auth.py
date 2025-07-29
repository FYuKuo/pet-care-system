from fastapi import Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from helpers.jwt_helper import decode_jwt_token

security = HTTPBearer()

def verify_access_token(request: Request) -> dict:

    # token = credentials.credentials
    # print(request.headers)

    token = request.cookies.get("accessToken")

    print(token)


    # 使用 helper 函數解碼和驗證 Token
    decoded_token = decode_jwt_token(token)

    return decoded_token

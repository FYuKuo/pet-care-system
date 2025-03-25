import jwt
import requests
from exceptions.custom_exceptions import UnauthorizedException
from config import config
import json


def get_cognito_public_key(kid: str):
    JWKS_URL = config.COGNITO_JWKS_URL
    JWKS = requests.get(JWKS_URL).json()

    """ 從 Cognito 取得對應的公鑰 """
    for key in JWKS["keys"]:
        if key["kid"] == kid:
            return key
    return None


def decode_jwt_token(token: str) -> dict:

    try:
        # 解析 JWT Header 取得 Key ID (kid)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # 取得 Cognito 公鑰
        public_key = get_cognito_public_key(kid)
        if not public_key:
            raise UnauthorizedException()
        
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))

        # 使用 Cognito 公鑰解碼 JWT
        decoded_token = jwt.decode(
            token,
            key=public_key,  # 公鑰
            algorithms=["RS256"],  # Cognito 預設使用 RS256
            issuer=config.COGNITO_ISSUER  # Token 發行者
        )

        return decoded_token  # 成功驗證後回傳 Token 內的資訊

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise UnauthorizedException()
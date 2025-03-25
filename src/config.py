import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    APP_NAME = "PetCareSystem"
    DEBUG = False
    AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
    COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
    COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
    S3_BUCKET = os.getenv("S3_BUCKET")
    COGNITO_ISSUER = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    COGNITO_JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

class DevConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False

ENV = os.getenv("ENV", "dev")
config = DevConfig if ENV == "dev" else ProdConfig
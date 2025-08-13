from pydantic import BaseModel, Field, EmailStr, conint
from typing import Optional
from enum import Enum
import time

class GenderEnum(str, Enum):
    FEMALE = "0"
    MALE = "1"

class UserSignUpRequest(BaseModel):
    name: str = Field(description="user name")
    email: EmailStr = Field(description="user email")
    password: str = Field(description="user password")

class UserSignUpResponse(BaseModel):
    userId: str
    name: str
    email: EmailStr

class ConfirmUserSignUpRequest(BaseModel):
    email: EmailStr = Field(description="user email")
    confirmCode: str = Field(description="confirm code")

class ConfirmUserSignUpResponse(BaseModel):
    email: EmailStr

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(description="user email")
    password: str = Field(description="user password")

class AuthTokens(BaseModel):
    accessToken: str = Field(validation_alias="AccessToken", description="Your user’s access token.")
    expiresIn: int = Field(validation_alias="ExpiresIn",description="The expiration period of the token in seconds.")
    tokenType: str = Field(validation_alias="TokenType",description="The intended use of the token, for example Bearer.")
    refreshToken: str = Field(validation_alias="RefreshToken",description="Your user’s refresh token.")
    idToken: str = Field(validation_alias="IdToken",description="Your user’s ID token.")
    expiresAt: Optional[int] = Field(None, description="The expiration time of the token.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expiresAt = int(time.time()) + self.expiresIn

class UserData(BaseModel):
    userId: str = Field(description="user id")
    name: str = Field(description="user name")
    email: str = Field(description="user email")
    gender: Optional[str] = Field(None, description="user gender")
    photo: Optional[str] = Field(None, description="user photo")

class UserLoginResponse(BaseModel):
    authTokens: AuthTokens


class UserLogoutRequest(BaseModel):
    refreshToken: str = Field(description="user refresh token")

class RefreshTokenRequest(BaseModel):
    refreshToken: str = Field(description="user refresh token")

class RefreshTokenResponse(BaseModel):
    authTokens: AuthTokens

class ResendConfirmationCodeRequest(BaseModel):
    email: EmailStr = Field(description="user email")

class ChangePasswordRequest(BaseModel):
    previousPassword: str = Field(description="previous password")
    proposedPassword: str = Field(description="proposed password")

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(description="user email")

class ConfirmForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(description="user email")
    confirmCode: str = Field(description="confirm code")
    password: str = Field(description="user password")

class UpdateUserProfileRequest(BaseModel):
    email: EmailStr = Field(None, description="user email")
    name: str = Field(None, description="user name")
    gender: GenderEnum = Field(None, description="user gender, 0: Female, 1: Male")



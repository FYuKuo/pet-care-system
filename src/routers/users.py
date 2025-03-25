from fastapi import APIRouter, Request
from schemas.user_schema import (
    UserSignUpRequest,
    UserSignUpResponse,
    ConfirmUserSignUpRequest,
    ConfirmUserSignUpResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserLogoutRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    ResendConfirmationCodeRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ConfirmForgotPasswordRequest,
    UserData
)
from services.user_service import UserService

router = APIRouter()


@router.post("/signup", response_model=UserSignUpResponse)
def user_sign_up(user_data: UserSignUpRequest):
    user_service = UserService()
    response = user_service.user_sign_up(user_data)

    return response


@router.post("/confirm_user_signup", response_model=ConfirmUserSignUpResponse)
def confirm_user_signup(user_data: ConfirmUserSignUpRequest):
    user_service = UserService()
    response = user_service.confirm_user_signup(user_data.email, user_data.confirmCode)

    return response


@router.post("/login", response_model=UserLoginResponse)
def login(user_data: UserLoginRequest):
    user_service = UserService()
    response = user_service.login(user_data.email, user_data.password)

    return response


@router.post("/logout")
def logout(user_data: UserLogoutRequest):

    user_service = UserService()
    user_service.logout(user_data.refreshToken)

    return {}

@router.post("/refresh_token_auth", response_model=RefreshTokenResponse)
def refresh_token_auth(user_data: RefreshTokenRequest):

    user_service = UserService()
    response = user_service.refresh_token(user_data.refreshToken)

    return response

@router.post("/resend_confirmation_code")
def resend_confirmation_code(user_data: ResendConfirmationCodeRequest):
    user_service = UserService()
    user_service.resend_confirmation_code(user_data.email)

    return {}

@router.post("/change_password")
def change_password(user_data: ChangePasswordRequest, request: Request):
    auth_header = request.headers.get("Authorization")
    access_token = auth_header.replace("Bearer ", "")

    user_service = UserService()
    user_service.change_password(user_data.previousPassword, user_data.proposedPassword, access_token)

    return {}

@router.post("/forgot_password")
def forgot_password(user_data: ForgotPasswordRequest):
    user_service = UserService()
    user_service.forgot_password(user_data.email)

    return {}

@router.post("/confirm_forgot_password")
def confirm_forgot_password(user_data: ConfirmForgotPasswordRequest):
    user_service = UserService()
    user_service.confirm_forgot_password(user_data.email, user_data.confirmCode, user_data.password)

    return {}

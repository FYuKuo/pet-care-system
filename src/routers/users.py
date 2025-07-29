from fastapi import APIRouter, Request, Depends, Response
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
    UserData,
    UpdateUserProfileRequest,
)
from services.user_service import UserService
from dependencies.auth import verify_access_token
from dependencies.permissions import check_user_permission
from utils.auth_cookie import AuthCookie

router = APIRouter()


@router.post("/auth/signup", response_model=UserSignUpResponse)
def user_sign_up(sign_up_data: UserSignUpRequest):
    user_service = UserService()
    response = user_service.user_sign_up(sign_up_data)

    return response


@router.post("/auth/confirm_user_signup", response_model=ConfirmUserSignUpResponse)
def confirm_user_signup(confirm_signup_data: ConfirmUserSignUpRequest):
    user_service = UserService()
    response = user_service.confirm_user_signup(
        confirm_signup_data.email, confirm_signup_data.confirmCode
    )

    return response


@router.post("/auth/login", response_model=UserLoginResponse)
def login(login_data: UserLoginRequest, response: Response):
    user_service = UserService()
    result = user_service.login(login_data.email, login_data.password)

    AuthCookie.set_login_cookies(response, result.authTokens.accessToken, result.authTokens.refreshToken, result.authTokens.expiresIn)

    return result


@router.post("/auth/logout")
def logout(
    request: Request,
    response: Response,
    user_claims: dict = Depends(verify_access_token),
):
    refresh_token = request.cookies.get("refreshToken")
    
    user_service = UserService()
    user_service.logout(refresh_token)

    AuthCookie.clear_auth_cookies(response)

    return {}


@router.post("/auth/refresh_token_auth")
def refresh_token_auth(request: Request, response: Response):

    refresh_token = request.cookies.get("refreshToken")

    user_service = UserService()
    result = user_service.refresh_token(refresh_token)

    AuthCookie.set_login_cookies(response, result.authTokens.accessToken, result.authTokens.refreshToken, result.authTokens.expiresIn)

    return result


@router.post("/auth/resend_confirmation_code")
def resend_confirmation_code(resend_code_data: ResendConfirmationCodeRequest):
    user_service = UserService()
    user_service.resend_confirmation_code(resend_code_data.email)

    return {}


@router.post("/change_password")
def change_password(
    change_password_data: ChangePasswordRequest,
    request: Request,
    user_claims: dict = Depends(verify_access_token),
):
    auth_header = request.headers.get("Authorization")
    access_token = auth_header.replace("Bearer ", "")

    user_service = UserService()
    user_service.change_password(
        change_password_data.previousPassword,
        change_password_data.proposedPassword,
        access_token,
    )

    return {}


@router.post("/auth/forgot_password")
def forgot_password(forgot_password_data: ForgotPasswordRequest):
    user_service = UserService()
    user_service.forgot_password(forgot_password_data.email)

    return {}


@router.post("/auth/confirm_forgot_password")
def confirm_forgot_password(confirm_forgot_password_data: ConfirmForgotPasswordRequest):
    user_service = UserService()
    user_service.confirm_forgot_password(
        confirm_forgot_password_data.email,
        confirm_forgot_password_data.confirmCode,
        confirm_forgot_password_data.password,
    )

    return {}


@router.get("/profile", response_model=UserData)
def get_user_profile(user_claims: dict = Depends(verify_access_token)):

    user_id = user_claims.get("sub")
    user_service = UserService()
    response = user_service.get_user_data(user_id)

    return response


@router.put("/{user_id}", response_model=UserData)
def update_user_profile(
    user_id: str,
    update_user_data: UpdateUserProfileRequest,
    user_claims: dict = Depends(check_user_permission),
):

    user_service = UserService()
    response = user_service.update_user_data(
        user_id, name=update_user_data.name, gender=update_user_data.gender
    )

    return response

@router.delete("/{user_id}", response_model=UserData)
def delete_user_profile(
    user_id: str,
    response: Response,
    user_claims: dict = Depends(check_user_permission),
):

    user_service = UserService()
    result = user_service.delete_user_data(user_id)

    AuthCookie.clear_auth_cookies(response)

    return result

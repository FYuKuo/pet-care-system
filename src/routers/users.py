from fastapi import APIRouter, Request, Depends
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

router = APIRouter()


@router.post("/signup", response_model=UserSignUpResponse)
def user_sign_up(sign_up_data: UserSignUpRequest):
    user_service = UserService()
    response = user_service.user_sign_up(sign_up_data)

    return response


@router.post("/confirm_user_signup", response_model=ConfirmUserSignUpResponse)
def confirm_user_signup(confirm_signup_data: ConfirmUserSignUpRequest):
    user_service = UserService()
    response = user_service.confirm_user_signup(
        confirm_signup_data.email, confirm_signup_data.confirmCode
    )

    return response


@router.post("/login", response_model=UserLoginResponse)
def login(login_data: UserLoginRequest):
    user_service = UserService()
    response = user_service.login(login_data.email, login_data.password)

    return response


@router.post("/logout")
def logout(
    logout_data: UserLogoutRequest,
    user_claims: dict = Depends(verify_access_token),
):
    user_service = UserService()
    user_service.logout(logout_data.refreshToken)

    return {}


@router.post("/refresh_token_auth", response_model=RefreshTokenResponse)
def refresh_token_auth(refresh_token_data: RefreshTokenRequest):

    user_service = UserService()
    response = user_service.refresh_token(refresh_token_data.refreshToken)

    return response


@router.post("/resend_confirmation_code")
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


@router.post("/forgot_password")
def forgot_password(forgot_password_data: ForgotPasswordRequest):
    user_service = UserService()
    user_service.forgot_password(forgot_password_data.email)

    return {}


@router.post("/confirm_forgot_password")
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
def update_user_profile(
    user_id: str,
    user_claims: dict = Depends(check_user_permission),
):

    user_service = UserService()
    response = user_service.delete_user_data(user_id)

    return response

from schemas.user_schema import (
    UserSignUpRequest,
    UserSignUpResponse,
    ConfirmUserSignUpResponse,
    UserLoginResponse,
    RefreshTokenResponse,
    UserData,
)
from services.cognito_service import CognitoService
from repositories.user_repository import UserRepository
from models.user_model import UserModel
from exceptions.custom_exceptions import NotFoundException
import time


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def user_sign_up(self, user_data: UserSignUpRequest):
        name = user_data.name
        email = user_data.email
        password = user_data.password
        current_time = int(time.time())

        cognito_service = CognitoService()

        # sign up in cognito
        res = cognito_service.sign_up(email, password, {"name": name})
        user_id = res.get("UserSub")

        # save user data to DB
        user_model = UserModel(
            user_id=user_id, email=email, name=name, created_at=current_time
        )

        self.user_repository.create_user(user_model.to_dict())

        return UserSignUpResponse(userId=user_id, name=name, email=email)

    def confirm_user_signup(self, email: str, confirm_code: str):
        cognito_service = CognitoService()
        cognito_service.confirm_sign_up(email, confirm_code)

        return ConfirmUserSignUpResponse(email=email)

    def login(self, email: str, password: str):
        cognito_service = CognitoService()
        res = cognito_service.initiate_auth(email, password)

        return UserLoginResponse(authTokens=res.get("AuthenticationResult"))

    def logout(self, refresh_token: str):
        cognito_service = CognitoService()
        cognito_service.revoke_token(refresh_token)

    def refresh_token(self, refresh_token: str):
        cognito_service = CognitoService()
        res = cognito_service.refresh_token(refresh_token)

        authentication_result = res.get("AuthenticationResult")
        authentication_result["RefreshToken"] = refresh_token

        return RefreshTokenResponse(authTokens=authentication_result)

    def resend_confirmation_code(self, email: str):
        cognito_service = CognitoService()
        cognito_service.resend_confirmation_code(email)

    def change_password(
        self, previous_password: str, proposed_password: str, access_token: str
    ):
        cognito_service = CognitoService()
        cognito_service.change_password(
            previous_password, proposed_password, access_token
        )

    def forgot_password(self, email: str):
        cognito_service = CognitoService()
        cognito_service.forgot_password(email)

    def confirm_forgot_password(self, email: str, confirm_code: str, password: str):
        cognito_service = CognitoService()
        cognito_service.confirm_forgot_password(email, confirm_code, password)

    def get_user_data(self, user_id):
        key = {"PK": f"USER#{user_id}", "SK": "PROFILE"}

        response = self.user_repository.get_user(key)

        if not response:
            raise NotFoundException(f"User {user_id}")
        
        return response

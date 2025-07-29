from utils import aws_clients
from config import config
from exceptions.custom_exceptions import (
    InvalidParameterException,
    AlreadyExistsException,
    UserNotConfirmedException,
    TooManyRequestsException,
    IncorrectLoginException,
    PermissionDeniedException,
)
import botocore

class CognitoService:
    def __init__(self):
        self.cognito_idp_client = aws_clients.get_cognito_idp_client()

    def sign_up(self, username: str, password: str, user_attributes: dict) -> dict:
        user_attributes_array = self._format_user_attributes(user_attributes)

        try:
            response = self.cognito_idp_client.sign_up(
                ClientId=config.COGNITO_CLIENT_ID,
                Username=username,
                Password=password,
                UserAttributes=user_attributes_array,
            )
        except self.cognito_idp_client.exceptions.UsernameExistsException as e:
            raise AlreadyExistsException(username)

        return response

    def confirm_sign_up(self, username: str, confirmation_code: str):
        try:
            response = self.cognito_idp_client.confirm_sign_up(
                ClientId=config.COGNITO_CLIENT_ID,
                Username=username,
                ConfirmationCode=confirmation_code,
            )
        except (
            self.cognito_idp_client.exceptions.InvalidParameterException,
            self.cognito_idp_client.exceptions.ExpiredCodeException,
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.CodeMismatchException,
            botocore.exceptions.ParamValidationError,
        ) as e:
            raise InvalidParameterException("ConfirmationCode", message=e)

        return response

    def initiate_auth(self, username: str, password: str) -> dict:
        try:
            response = self.cognito_idp_client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                },
                ClientId=config.COGNITO_CLIENT_ID,
            )
        except (
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.UserNotFoundException,
            self.cognito_idp_client.exceptions.InvalidParameterException,
        ) as e:
            if 'Password attempts exceeded' in str(e):
                raise TooManyRequestsException()
            raise IncorrectLoginException()
        except self.cognito_idp_client.exceptions.UserNotConfirmedException as e:
            raise UserNotConfirmedException()
        except self.cognito_idp_client.exceptions.TooManyRequestsException as e:
            raise TooManyRequestsException()

        return response
    
    def refresh_token(self, refresh_token: str) -> dict:
        try:
            response = self.cognito_idp_client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                },
                ClientId=config.COGNITO_CLIENT_ID,
            )
        except (
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.UserNotFoundException,
            self.cognito_idp_client.exceptions.InvalidParameterException,
        ) as e:
            raise PermissionDeniedException()
        except self.cognito_idp_client.exceptions.UserNotConfirmedException as e:
            raise UserNotConfirmedException()
        except self.cognito_idp_client.exceptions.TooManyRequestsException as e:
            raise TooManyRequestsException()

        return response

    def revoke_token(self, token: str):
        try:
            response = self.cognito_idp_client.revoke_token(
                Token=token,
                ClientId=config.COGNITO_CLIENT_ID,
            )
        except self.cognito_idp_client.exceptions.TooManyRequestsException as e:
            raise TooManyRequestsException()
        except self.cognito_idp_client.exceptions.InvalidParameterException as e:
            raise InvalidParameterException("Refresh Token", message=e)

        return response

    def forgot_password(self, username: str):
        try:
            response = self.cognito_idp_client.forgot_password(
                ClientId=config.COGNITO_CLIENT_ID,
                Username=username,
            )
        except (
            self.cognito_idp_client.exceptions.TooManyRequestsException,
            self.cognito_idp_client.exceptions.LimitExceededException,
        ) as e:
            raise TooManyRequestsException()
        except self.cognito_idp_client.exceptions.UserNotConfirmedException as e:
            raise UserNotConfirmedException()

        return response

    def confirm_forgot_password(self, username: str, confirmation_code: str, password: str):
        try:
            response = self.cognito_idp_client.confirm_forgot_password(
                ClientId=config.COGNITO_CLIENT_ID,
                Username=username,
                ConfirmationCode=confirmation_code,
                Password=password
            )
        except (
            self.cognito_idp_client.exceptions.TooManyRequestsException,
            self.cognito_idp_client.exceptions.LimitExceededException,
        ) as e:
            raise TooManyRequestsException()
        except (
            self.cognito_idp_client.exceptions.InvalidParameterException,
            self.cognito_idp_client.exceptions.ExpiredCodeException,
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.CodeMismatchException,
            botocore.exceptions.ParamValidationError,
        ) as e:
            raise InvalidParameterException("ConfirmationCode", message=e)
        except self.cognito_idp_client.exceptions.InvalidPasswordException as e:
            raise InvalidParameterException("Password", message=e)
        except self.cognito_idp_client.exceptions.UserNotConfirmedException as e:
            raise UserNotConfirmedException()

        return response

    def change_password(self, previous_password: str, proposed_password: str, access_token: str):
        try:
            response = self.cognito_idp_client.change_password(
                PreviousPassword=previous_password,
                ProposedPassword=proposed_password,
                AccessToken=access_token
            )
        except (
            self.cognito_idp_client.exceptions.TooManyRequestsException,
            self.cognito_idp_client.exceptions.LimitExceededException,
        ) as e:
            raise TooManyRequestsException()
        except (
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.UserNotFoundException,
            self.cognito_idp_client.exceptions.InvalidParameterException,
        ) as e:
            raise InvalidParameterException("previousPassword", message=e)
        except self.cognito_idp_client.exceptions.InvalidPasswordException as e:
            raise InvalidParameterException("proposedPassword", message=e)
        except self.cognito_idp_client.exceptions.UserNotConfirmedException as e:
            raise UserNotConfirmedException()

        return response


    def resend_confirmation_code(self, username: str):
        try:
            response = self.cognito_idp_client.resend_confirmation_code(
                ClientId=config.COGNITO_CLIENT_ID,
                Username=username,
            )
        except (
            self.cognito_idp_client.exceptions.InvalidParameterException,
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.UserNotFoundException,
        ) as e:
            raise PermissionDeniedException()
        except (
            self.cognito_idp_client.exceptions.TooManyRequestsException,
            self.cognito_idp_client.exceptions.LimitExceededException,
        ) as e:
            raise TooManyRequestsException()

        return response
    
    def update_user_attributes(self, username: str, user_attributes: dict):
        user_attributes_array = self._format_user_attributes(user_attributes)

        try:
            response = self.cognito_idp_client.admin_update_user_attributes(
                UserPoolId=config.COGNITO_USER_POOL_ID,
                Username=username,
                UserAttributes=user_attributes_array,
            )
        except (
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.UserNotFoundException,
        ) as e:
            raise PermissionDeniedException()
        except (
            self.cognito_idp_client.exceptions.TooManyRequestsException,
        ) as e:
            raise TooManyRequestsException()

        return response
    
    def delete_user(self, username: str):

        try:
            response = self.cognito_idp_client.admin_delete_user(
                UserPoolId=config.COGNITO_USER_POOL_ID,
                Username=username,
            )
        except (
            self.cognito_idp_client.exceptions.NotAuthorizedException,
            self.cognito_idp_client.exceptions.UserNotFoundException,
        ) as e:
            raise PermissionDeniedException()
        except (
            self.cognito_idp_client.exceptions.TooManyRequestsException,
        ) as e:
            raise TooManyRequestsException()

        return response


    def _format_user_attributes(self, user_attributes: dict) -> list:
        return [{"Name": key, "Value": value} for key, value in user_attributes.items()]
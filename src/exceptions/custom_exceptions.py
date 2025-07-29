class BaseException(Exception):
    def __init__(self, error: str, message: str, status_code: int):
        self.error = error
        self.message = message
        self.status_code = status_code


class NotFoundException(BaseException):
    def __init__(self, resource_name: str):
        super().__init__(
            error="RESOURCE NOT FOUND",
            message=f"{resource_name} not found",
            status_code=404,
        )


class AlreadyExistsException(BaseException):
    def __init__(self, resource_name: str):
        super().__init__(
            error="RESOURCE ALREADY EXISTS",
            message=f"{resource_name} already exists",
            status_code=400,
        )


class PermissionDeniedException(BaseException):
    def __init__(self):
        super().__init__(
            error="PERMISSION DENIED",
            message=f"You do not have permission to perform this action. Please check your permissions",
            status_code=403,
        )


class MissingParameterException(BaseException):
    def __init__(self, parameter_name: str):
        super().__init__(
            error="MISSING PARAMETER",
            message=f"Missing required parameter: {parameter_name}",
            status_code=400,
        )


class InvalidParameterException(BaseException):
    def __init__(self, parameter_name: str, *, message: str = None):
        error_message = f"Invalid parameter: {parameter_name}"
        if message:
            error_message = error_message + f", {message}"

        super().__init__(
            error="INVALID PARAMETER",
            message=error_message,
            status_code=400,
        )


class UserNotConfirmedException(BaseException):
    def __init__(self):
        super().__init__(
            error="USER NOT CONFIRMED",
            message="user not confirmed",
            status_code=401,
        )

class TooManyRequestsException(BaseException):
    def __init__(self):
        super().__init__(
            error="TOO MANY REQUESTS",
            message="You have sent too many requests in a short period. Please try again later.",
            status_code=429,
        )

class IncorrectLoginException(BaseException):
    def __init__(self):
        super().__init__(
            error="Unauthorized",
            message="Invalid username or password.",
            status_code=401,
        )

class UnauthorizedException(BaseException):
    def __init__(self):
        super().__init__(
            error="Unauthorized",
            message="Invalid token.",
            status_code=401,
        )

class InternalErrorException(BaseException):
    def __init__(self):
        super().__init__(
            error="INTERNAL SERVER ERROR",
            message="Internal server error.",
            status_code=500,
        )


class DBConditionalCheckFailedException(Exception):
    def __init__(self):
        super().__init__()

class DBException(Exception):
    def __init__(self):
        super().__init__()
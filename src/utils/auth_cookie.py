from fastapi import Response


class AuthCookie:

    @staticmethod
    def set_login_cookies(
        response: Response,
        access_token: str,
        refresh_token: str,
        access_token_expires: int,
        *,
        refresh_token_expires: int = 604800,
    ) -> None:
        response.set_cookie(
            key="accessToken",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/",
            expires=access_token_expires,
        )

        response.set_cookie(
            key="refreshToken",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/",
            expires=refresh_token_expires,
        )

    @staticmethod
    def clear_auth_cookies(response: Response) -> None:
        response.delete_cookie(
            key="accessToken", httponly=True, secure=True, samesite="none", path="/"
        )
        response.delete_cookie(
            key="refreshToken", httponly=True, secure=True, samesite="none", path="/"
        )

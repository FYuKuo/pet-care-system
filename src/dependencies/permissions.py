from fastapi import HTTPException, Depends
from dependencies.auth import verify_access_token
from exceptions.custom_exceptions import PermissionDeniedException

def check_user_permission(
    user_id: str,  # 這裡會自動接收到路由中的 user_id
    user_claims: dict = Depends(verify_access_token)
):
    if user_id != user_claims.get("sub"):
        raise PermissionDeniedException()
    return user_claims
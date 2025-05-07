from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from starlette.requests import Request

from schema.user import UserOutputSchema


def is_authenticated(request: Request) -> UserOutputSchema:
    if not request.user.is_authenticated:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not request.user.is_active:
        raise HTTPException(status_code=401, detail="User is not active")
    return request.user


def is_admin(
    user: Annotated[UserOutputSchema, Depends(is_authenticated)],
) -> UserOutputSchema:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not admin")
    return user


def is_service(
    user: Annotated[UserOutputSchema, Depends(is_authenticated)],
) -> UserOutputSchema:
    if not user.is_service:
        raise HTTPException(status_code=403, detail="User is not service")
    return user


def is_admin_or_service(
    user: Annotated[UserOutputSchema, Depends(is_authenticated)],
):
    if not user.is_admin and not user.is_service:
        raise HTTPException(status_code=403, detail="User is not admin or service")
    return user

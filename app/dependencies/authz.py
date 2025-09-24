from app.dependencies.authn import is_authenticated
from fastapi import Depends, HTTPException, status
from typing import Annotated


def has_roles(roles):
    def check_roles(user: Annotated[dict, Depends(is_authenticated)]):
        if user["role"] not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Access denied!")
        return user

    return check_roles

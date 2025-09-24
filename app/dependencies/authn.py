import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt


def is_authenticated(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    try:
        payload = jwt.decode(
            jwt=authorization.credentials,
            key=os.getenv("JWT_SECRET_KEY"),
            algorithms=["HS256"],
        )
        print(payload)
        return {"id": payload["id"], "role": payload["role"]}
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

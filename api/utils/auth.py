from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt


class AuthError(Exception):
    def __init__(self, error, status_code=401):
        self.error = error
        self.status_code = status_code


class Auth:
    def __init__(self):
        pass

    def __call__(
        self,
        request: Request,
        authorization: HTTPAuthorizationCredentials = Security(
            HTTPBearer(auto_error=False)
        ),
    ):

        if not authorization:
            raise HTTPException(
                403, 'not auth'
            )

        token = authorization.credentials
        payload = jwt.decode(token, "token", algorithms=["HS256"])

        return payload
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import verify_token
from errors.error_instance import error_instance

class jwtBearer(HTTPBearer):
    def __int__(self, auto_Error=True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        request_method = request.method
        request_route = request.url.components.path
        if credentials:
            if not credentials.scheme == "Bearer":
                error_instance(403, "Inválid or Expired Token!")
            permition = self.verify_jwt(credentials.credentials, request_method, request_route)
            if not permition:
                error_instance(403, "Inválid or Expired Token!")
            return credentials.credentials
        else:
            error_instance(403, "Inválid or Expired Token!")

    def verify_jwt(self, jwtoken, request_method, request_route):
        is_token_valid = False
        payload = verify_token(jwtoken, request_method, request_route)
        if payload:
            is_token_valid = True
        return is_token_valid

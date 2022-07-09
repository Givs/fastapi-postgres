from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __int__(self, auto_Error=True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        request_method = request.method
        request_route = request.url.components.path
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Inválid or Expired Token!")
            permition = self.verify_jwt(credentials.credentials, request_method, request_route)
            if not permition:
                raise HTTPException(status_code=403, detail="Inválid or Expired Token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Inválid or Expired Token!")

    def verify_jwt(self, jwtoken, request_method, request_route):
        is_token_valid = False
        payload = decodeJWT(jwtoken, request_method, request_route)
        if payload:
            is_token_valid = True
        return is_token_valid

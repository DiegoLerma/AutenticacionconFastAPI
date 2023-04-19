from utils.jwt_manager import validate_token # Importamos create_token, esto es para que cuando se haga una petición POST a la ruta /login se ejecute la función login
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data= validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales no son validas")
        

from fastapi import APIRouter
from fastapi.responses import JSONResponse # Importamos HTMLResponse, esto es para que cuando se haga una petición GET a la ruta / se muestre un HTML
# Importamos JSONResponse, esto es para que cuando se haga una petición GET a la ruta /movies se muestre un JSON
from pydantic import BaseModel # Importamos BaseModel, esto es para que cuando se haga una petición POST a la ruta /movies se valide el body de la petición
from utils.jwt_manager import create_token # Importamos create_token, esto es para que cuando se haga una petición POST a la ruta /login se ejecute la función login
# from fastapi.security import HTTPBearer
# from sqlmodel import Field, SQLModel, Session, engine
from schemas.user import User

user_router = APIRouter()

# Login
@user_router.post('/login', tags=['auth']) # Creamos una ruta con el decorador @user_router.post para el método POST, esto es para que cuando se haga una petición POST a la ruta /login se ejecute la función login
def login(user: User): # El parámetro user es para que se muestre en la documentación de la ruta
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)

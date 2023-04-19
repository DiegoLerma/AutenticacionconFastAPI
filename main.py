from fastapi import FastAPI # Importamos FastAPI, esto es para crear la instancia de FastAPI
# Path se usa para validar los parámetros de la ruta
# Query se usa para validar los parámetros de la query
# Importamos Query, esto es para que cuando se haga una petición GET a la ruta /movies/ se valide el parámetro category
from fastapi.responses import HTMLResponse, JSONResponse # Importamos HTMLResponse, esto es para que cuando se haga una petición GET a la ruta / se muestre un HTML
# Importamos JSONResponse, esto es para que cuando se haga una petición GET a la ruta /movies se muestre un JSON
from pydantic import BaseModel # Importamos BaseModel, esto es para que cuando se haga una petición POST a la ruta /movies se valide el body de la petición
from utils.jwt_manager import create_token # Importamos create_token, esto es para que cuando se haga una petición POST a la ruta /login se ejecute la función login
# from fastapi.security import HTTPBearer
from config.database import Base, engine
# from sqlmodel import Field, SQLModel, Session, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI() # Creamos una instancia de FastAPI
app.title = "Autenticador" # Asignamos un título a la instancia de FastAPI
app.description = "Autenticador de usuarios con FastAPI" # Asignamos una descripción a la instancia de FastAPI
app.version = "0.0.01" # Asignamos una versión a la instancia de FastAPI

app.add_middleware(ErrorHandler) # Agregamos el middleware errorHandler a la instancia de FastAPI
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine) # Creamos las tablas en la base de datos


# Lista de peliculas
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'    
    },
    {
        'id': 2,
        'title': 'Mario Bros',
        'overview': "Es el reino de los hongos, donde los hongos son los reyes ...",
        'year': '2023',
        'rating': 9.1,
        'category': 'Animada'    
    },
]


# Ruta principal
@app.get('/', tags=['home']) # Creamos una ruta con el decorador @app.get para el método GET, esto es para que cuando se haga una petición GET a la ruta / se ejecute la función message
# El parámetro tags es para que se muestre en la documentación de la ruta
def message(): # Creamos la función message
    return HTMLResponse("<h1>Autenticador</h1>") # Retornamos un HTML con el título Autenticador


from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends, Body # Importamos FastAPI, esto es para crear la instancia de FastAPI
# Path se usa para validar los parámetros de la ruta
# Query se usa para validar los parámetros de la query
# Importamos Query, esto es para que cuando se haga una petición GET a la ruta /movies/ se valide el parámetro category
from fastapi.responses import HTMLResponse, JSONResponse # Importamos HTMLResponse, esto es para que cuando se haga una petición GET a la ruta / se muestre un HTML
# Importamos JSONResponse, esto es para que cuando se haga una petición GET a la ruta /movies se muestre un JSON
from pydantic import BaseModel, Field # Importamos BaseModel, esto es para que cuando se haga una petición POST a la ruta /movies se valide el body de la petición
from typing import Optional, List # Importamos Optional, esto es para que cuando se haga una petición PUT a la ruta /movies/{movie_id} se valide el body de la petición
from jwt_manager import create_token, validate_token # Importamos create_token, esto es para que cuando se haga una petición POST a la ruta /login se ejecute la función login
from fastapi.security import HTTPBearer

app = FastAPI() # Creamos una instancia de FastAPI
app.title = "Autenticador" # Asignamos un título a la instancia de FastAPI
app.description = "Autenticador de usuarios con FASTAPI" # Asignamos una descripción a la instancia de FastAPI
app.version = "0.0.01" # Asignamos una versión a la instancia de FastAPI


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data= validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales no son validas")
        


# Modelo de datos para validar el body de la petición
class User(BaseModel): # Creamos una clase User que hereda de BaseModel
    email: str  
    password: str  


class Movie(BaseModel): # Creamos una clase Movie que hereda de BaseModel
    id: Optional[int] = None # El id es opcional, esto permite que cuando se haga una petición PUT a la ruta /movies/{movie_id} no se envíe el id
    title: str = Field(min_length=5, max_length=15) # El título es un string y tiene un máximo de 15 caracteres
    overview: str =Field(min_length=15, max_length=50)
    year: int=Field(le=2024)
    rating: float=Field(ge=0, le=10)
    category: str=Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 8,
                "category": "Categoria"
            }
        }


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


# Login
@app.post('/login', tags=['auth']) # Creamos una ruta con el decorador @app.post para el método POST, esto es para que cuando se haga una petición POST a la ruta /login se ejecute la función login
def login(user: User): # El parámetro user es para que se muestre en la documentación de la ruta
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)



# Ver todas las peliculas
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())]) # Creamos una ruta con el decorador @app.get para el método GET, esto es para que cuando se haga una petición GET a la ruta /movies se ejecute la función movies
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200) # Retornamos un JSON con el listado de películas


# Ver una pelicula por id
@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200) # Creamos una ruta con el decorador @app.get para el método GET, esto es para que cuando se haga una petición GET a la ruta /movies/{movie_id} se ejecute la función get_movie
def get_movie(id: int = Path(ge =1, le=2000))->Movie: # El parámetro movie_id es para que se muestre en la documentación de la ruta
    for movie in movies:
        if movie['id'] == id:
            return JSONResponse(content=movie, status_code=200)
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404)


# Ver peliculas por categoria
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200) # Creamos una ruta con el decorador @app.get para el método GET
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]: # El parámetro category es para que se muestre en la documentación de la ruta
    movies_by_category = []
    for movie in movies:
        if movie['category'] == category:
            movies_by_category.append(movie)
            return movies_by_category
    else:
        return JSONResponse(content={'message': 'Category not found'}, status_code=404)
    # data=[item for item in movies if item['category'] == category]
    # return JSONResponse(content=data, status_code=200)


# Crear una pelicula
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201) # Creamos una ruta con el decorador @app.post para el método POST
def create_movie(movie: Movie) -> dict: # El parámetro movie es para que se muestre en la documentación de la ruta
    movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado la pelicula"}, status_code=201)


# Actualizar una pelicula
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200) # Creamos una ruta con el decorador @app.put para el método PUT
def update_movie(id: int, movie:Movie)-> dict: # El parámetro movie es para que se muestre en la documentación de la ruta
    for movie_item in movies: # Recorremos la lista de películas
        if movie_item['id'] == id: # Si el id de la película es igual al id que se envía por parámetro
            movie_item['title'] = movie.title # Actualizamos el título de la película
            movie_item['overview'] = movie.overview
            movie_item['year'] = movie.year
            movie_item['rating'] = movie.rating
            movie_item['category'] = movie.category
            return JSONResponse(content={"message": "Se ha modificado la pelicula"}, status_code=200) # Retornamos la película actualizada
    return JSONResponse(content={"message": "No se ha encontrado la pelicula"}, status_code=404) # Retornamos un mensaje de película no encontrada


# Eliminar una pelicula
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200) # Creamos una ruta con el decorador @app.delete para el método DELETE
def delete_movie(id:int)-> dict: # El parámetro movie_id es para que se muestre en la documentación de la ruta
    for movie in movies: # Recorremos la lista de películas
        if movie['id'] == id: # Si el id de la película es igual al id que se envía por parámetro
            movies.remove(movie) # Eliminamos la película
            return JSONResponse(content={'message': 'Movie deleted'}, status_code=200) # Retornamos un mensaje de película eliminada
    return JSONResponse(content={'message': 'Movie not found'}, status_code=404) # Retornamos un mensaje de película no encontrada
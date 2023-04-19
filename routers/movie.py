from fastapi import APIRouter
from fastapi import Path, Query, Depends # Importamos FastAPI, esto es para crear la instancia de FastAPI
# Path se usa para validar los parámetros de la ruta
# Query se usa para validar los parámetros de la query
from fastapi.responses import JSONResponse # Importamos HTMLResponse, esto es para que cuando se haga una petición GET a la ruta / se muestre un HTML
from pydantic import BaseModel, Field # Importamos BaseModel, esto es para que cuando se haga una petición POST a la ruta /movies se valide el body de la petición
from typing import Optional, List # Importamos Optional, esto es para que cuando se haga una petición PUT a la ruta /movies/{movie_id} se valide el body de la petición
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


# Ver todas las peliculas
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())]) # Creamos una ruta con el decorador @movie_router.get para el método GET, esto es para que cuando se haga una petición GET a la ruta /movies se ejecute la función movies
def get_movies() -> List[Movie]:
    db=Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200) # Retornamos un JSON con el listado de películas


# Ver una pelicula por id
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200) # Creamos una ruta con el decorador @movie_router.get para el método GET, esto es para que cuando se haga una petición GET a la ruta /movies/{movie_id} se ejecute la función get_movie
def get_movie(id: int = Path(ge =1, le=2000))->Movie: # El parámetro movie_id es para que se muestre en la documentación de la ruta
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Ver peliculas por categoria
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200) # Creamos una ruta con el decorador @movie_router.get para el método GET
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]: # El parámetro category es para que se muestre en la documentación de la ruta
    db=Session()
    result=MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Category not found"})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    # movies_by_category = []
    # for movie in movies:
    #     if movie['category'] == category:
    #         movies_by_category.append(movie)
    #         return movies_by_category
    # else:
    #     return JSONResponse(content={'message': 'Category not found'}, status_code=404)
    # data=[item for item in movies if item['category'] == category]
    # return JSONResponse(content=data, status_code=200)


# Crear una pelicula
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201) # Creamos una ruta con el decorador @movie_router.post para el método POST
def create_movie(movie: Movie) -> dict: # El parámetro movie es para que se muestre en la documentación de la ruta
    db=Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Se ha registrado la pelicula"}, status_code=201)


# Actualizar una pelicula
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200) # Creamos una ruta con el decorador @movie_router.put para el método PUT
def update_movie(id: int, movie:Movie)-> dict: # El parámetro movie es para que se muestre en la documentación de la ruta
    db=Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "Se ha modificado la pelicula"}, status_code=200)
    
    # for movie_item in movies: # Recorremos la lista de películas
    #     if movie_item['id'] == id: # Si el id de la película es igual al id que se envía por parámetro
    #         movie_item['title'] = movie.title # Actualizamos el título de la película
    #         movie_item['overview'] = movie.overview
    #         movie_item['year'] = movie.year
    #         movie_item['rating'] = movie.rating
    #         movie_item['category'] = movie.category
    #         return JSONResponse(content={"message": "Se ha modificado la pelicula"}, status_code=200) # Retornamos la película actualizada
    # return JSONResponse(content={"message": "No se ha encontrado la pelicula"}, status_code=404) # Retornamos un mensaje de película no encontrada


# Eliminar una pelicula
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200) # Creamos una ruta con el decorador @movie_router.delete para el método DELETE
def delete_movie(id:int)-> dict: # El parámetro movie_id es para que se muestre en la documentación de la ruta
    db=Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "Se ha eliminado la pelicula"}, status_code=200)
    
    # for movie in movies: # Recorremos la lista de películas
    #     if movie['id'] == id: # Si el id de la película es igual al id que se envía por parámetro
    #         movies.remove(movie) # Eliminamos la película
    #         return JSONResponse(content={'message': 'Movie deleted'}, status_code=200) # Retornamos un mensaje de película eliminada
    # return JSONResponse(content={'message': 'Movie not found'}, status_code=404) # Retornamos un mensaje de película no encontrada
from fastapi import FastAPI, Body # Importamos FastAPI
from fastapi.responses import HTMLResponse # Importamos HTMLResponse, esto es para que cuando se haga una petición GET a la ruta / se muestre un HTML
from pydantic import BaseModel, Field # Importamos BaseModel, esto es para que cuando se haga una petición POST a la ruta /movies se valide el body de la petición
from typing import Optional # Importamos Optional, esto es para que cuando se haga una petición PUT a la ruta /movies/{movie_id} se valide el body de la petición

app = FastAPI() # Creamos una instancia de FastAPI
app.title = "Autenticador" # Asignamos un título a la instancia de FastAPI
app.description = "Autenticador de usuarios con FASTAPI" # Asignamos una descripción a la instancia de FastAPI
app.version = "0.0.01" # Asignamos una versión a la instancia de FastAPI

class Movie(BaseModel): # Creamos una clase Movie que hereda de BaseModel
    id: Optional[int] = None # El id es opcional, esto permite que cuando se haga una petición PUT a la ruta /movies/{movie_id} no se envíe el id
    title: str = Field(min_length=5, max_length=15) # El título es un string y tiene un máximo de 15 caracteres
    overview: str =Field(min_length=15, max_length=50)
    year: int=Field(le=2024)
    rating: float
    category: str

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

@app.get('/', tags=['home']) # Creamos una ruta con el decorador @app.get para el método GET, esto es para que cuando se haga una petición GET a la ruta / se ejecute la función message
# El parámetro tags es para que se muestre en la documentación de la ruta

def message(): # Creamos la función message
    return HTMLResponse("<h1>Autenticador</h1>") # Retornamos un HTML con el título Autenticador

@app.get('/movies', tags=['movies']) # Creamos una ruta con el decorador @app.get para el método GET, esto es para que cuando se haga una petición GET a la ruta /movies se ejecute la función movies
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies']) # Creamos una ruta con el decorador @app.get para el método GET, esto es para que cuando se haga una petición GET a la ruta /movies/{movie_id} se ejecute la función get_movie
def get_movie(id: int): # El parámetro movie_id es para que se muestre en la documentación de la ruta
    for movie in movies:
        if movie['id'] == id:
            return movie
    return []

@app.get('/movies/', tags=['movies']) # Creamos una ruta con el decorador @app.get para el método GET
def get_movies_by_category(category: str): # El parámetro category es para que se muestre en la documentación de la ruta
    # movies_by_category = []
    # for movie in movies:
    #     if movie['category'] == category:
    #         movies_by_category.append(movie)
    # return movies_by_category

    return [item for item in movies if item['category'] == category]

@app.post('/movies', tags=['movies']) # Creamos una ruta con el decorador @app.post para el método POST
def create_movie(movie: Movie): # El parámetro movie es para que se muestre en la documentación de la ruta
    movies.append(movie)
    return movies

@app.put('/movies/{id}', tags=['movies']) # Creamos una ruta con el decorador @app.put para el método PUT
def update_movie(id: int, movie:Movie): # El parámetro movie es para que se muestre en la documentación de la ruta
    for movie_item in movies: # Recorremos la lista de películas
        if movie_item['id'] == id: # Si el id de la película es igual al id que se envía por parámetro
            movie_item['title'] = movie.title # Actualizamos el título de la película
            movie_item['overview'] = movie.overview
            movie_item['year'] = movie.year
            movie_item['rating'] = movie.rating
            movie_item['category'] = movie.category
            return movies # Retornamos la película actualizada

@app.delete('/movies/{id}', tags=['movies']) # Creamos una ruta con el decorador @app.delete para el método DELETE
def delete_movie(id:int): # El parámetro movie_id es para que se muestre en la documentación de la ruta
    for movie in movies: # Recorremos la lista de películas
        if movie['id'] == id: # Si el id de la película es igual al id que se envía por parámetro
            movies.remove(movie) # Eliminamos la película
            return movies # Retornamos la lista de películas
        else:
            return "No existe la película con ese id"
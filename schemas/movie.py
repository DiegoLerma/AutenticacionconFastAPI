from pydantic import BaseModel, Field
from typing import Optional

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

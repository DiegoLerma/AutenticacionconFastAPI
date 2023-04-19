from pydantic import BaseModel

# Modelo de datos para validar el body de la petición
class User(BaseModel): # Creamos una clase User que hereda de BaseModel
    email: str  
    password: str  
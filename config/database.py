import os # Este módulo nos permite acceder a las rutas del sistema operativo
from sqlalchemy import create_engine # Create_engine es una función que nos permite crear una conexión a la base de datos
from sqlalchemy.orm.session import sessionmaker # Sessionmaker es una función que nos permite crear una sesión para hacer consultas a la base de datos
from sqlalchemy.ext.declarative import declarative_base # Declarative_base es una función que nos permite crear una clase base para nuestros modelos

sqlite_file_name='../database.sqlite' # Nombre del archivo de la base de datos
base_dir=os.path.dirname(os.path.realpath(__file__)) # Ruta del directorio actual

database_url=f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" # Ruta de la base de datos uniendo la ruta del directorio actual con el nombre del archivo de la base de datos

engine=create_engine(database_url, echo=True) # Creamos la conexión a la base de datos con la función create_engine

Session = sessionmaker(bind=engine) # Creamos la sesión con la función sessionmaker

Base = declarative_base() # Creamos la clase base para nuestros modelos
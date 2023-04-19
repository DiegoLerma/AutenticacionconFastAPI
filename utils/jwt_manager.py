from jwt import encode, decode

def create_token(data:dict) -> str: # Esta funcion crea el token
    token:str=encode(payload=data, key="my_secret_key", algorithm="HS256") # El payload es el diccionario que contiene los datos que queremos guardar en el token
    # El key es la clave secreta que usaremos para encriptar el token
    # El algoritmo es el algoritmo que usaremos para encriptar el token
    # El token es un string que contiene los datos encriptados
    # El algoritmo HS256 es el algoritmo de encriptación más seguro
    return token

def validate_token(token:str)->dict: # Esta funcion valida el token
    data:dict=decode(token, key="my_secret_key", algorithms=["HS256"]) #Con decode decodificamos el token, tiene por parametros el token, la clave secreta y el algoritmo
    return data
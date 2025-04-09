from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
# Se añaden para funcionar con el front
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "https://https://pokeapi-uv.onrender.com/",
    "http://localhost:8000",  # Para desarrollo local
    "http://127.0.0.1:8000/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en desarrollo) para probar en local
    #allow_origins=origins, # Permite todos los orígenes (en desarrollo) para la web
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)
class Pokemon(BaseModel):
    id: int
    nombre: str
    vida: int
    daño: int
    defensa: int

# POKEMONES PRINCIPALES
bulbasaur = {
    "id": 1,
    "nombre": "bulbasaur",
    "vida": 45,
    "daño": 49,
    "defensa": 49
}
charmander = {
    "id": 4,
    "nombre": "charmander",
    "vida": 39,
    "daño": 52,
    "defensa": 43
}
squirtle = {
    "id": 7,
    "nombre": "squirtle",
    "vida": 44,
    "daño": 48,
    "defensa": 65
}
pokemones = [bulbasaur, charmander, squirtle]

# Nueva ruta para servir el HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("pokemons.html", {"request": request})

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pokemons/")
async def retornar_todos_pokemones():
    return {"Pokemones": pokemones}

#Vamos a tener en cuenta que no se pueden crear pokemones con ID negativas o menores a 0
@app.get("/pokemons/{pokemon_id}")
def read_pokemon(pokemon_id: int):
    if pokemon_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID debe ser un entero positivo mayor a 0"
        )
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            return pokemon
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pokémon con ID {pokemon_id} no encontrado"
    )

#Vamos a tener en cuenta que no se pueden crear pokemones con ID negativas o menores a 0
#Tampoco se permite vida menor a 1, ni daño y defensa menores a 0
@app.post("/pokemons/")
def create_pokemon(pokemon: Pokemon):
    if pokemon.id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID debe ser un entero positivo mayor a 0"
        )
    if pokemon.vida <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La vida debe ser un entero positivo mayor a 0"
        )
    if pokemon.daño < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El daño debe ser un entero mayor o igual a 0"
        )
    if pokemon.defensa < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La defensa debe ser un entero mayor o igual a 0"
        )
    pokemon_dict = pokemon.dict()
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_dict["id"]:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un Pokémon con ID {pokemon['id']}"
        )
    pokemones.append(pokemon_dict)
    return {"Pokemon añadido": {"Pokemon": pokemon_dict}}
    

#Vamos a tener en cuenta que no se pueden crear pokemones con ID negativas o menores a 0
#Tampoco podemos permitir que se cambie una ID por la ID ya existente de otro Pokemon
#Tampoco se permite vida menor a 1, ni daño y defensa menores a 0
@app.put("/pokemons/{pokemon_id}")
def update_pokemon(pokemon_id: int, nuevo_pokemon: Pokemon):
    if nuevo_pokemon.id != pokemon_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cambiar la ID del Pokemon"
        )
    if nuevo_pokemon.id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID debe ser un entero positivo mayor a 0"
        )
    if nuevo_pokemon.vida <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La vida debe ser un entero positivo mayor a 0"
        )
    if nuevo_pokemon.daño < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El daño debe ser un entero mayor o igual a 0"
        )
    if nuevo_pokemon.defensa < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La defensa debe ser un entero mayor o igual a 0"
        )
    nuevo_pokemon_dict = nuevo_pokemon.dict()
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            pokemon.update(nuevo_pokemon_dict)
            return{"Éxito": "Pokemon actualizado"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pokémon con ID {pokemon_id} no encontrado"
    )

#Vamos a tener en cuenta que no existen pokemones con ID negativas o menores a 0
@app.delete("/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    if pokemon_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID debe ser un entero positivo mayor a 0"
        )
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            pokemones.remove(pokemon)
            return{"Éxito": "Pokemon Eliminado"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pokémon con ID {pokemon_id} no encontrado"
    )
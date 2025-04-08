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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (en desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)
class Pokemon(BaseModel):
    id: int
    nombre: str
    vida: float
    daño: float
    defensa: float

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

@app.get("/pokemons/{pokemon_id}")
def read_pokemon(pokemon_id: int):
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            return pokemon
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pokémon con ID {pokemon_id} no encontrado"
    )

@app.post("/pokemons/")
def create_pokemon(pokemon: Pokemon):
    pokemon_dict = pokemon.dict()
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_dict["id"]:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un Pokémon con ID {pokemon['id']}"
        )
    pokemones.append(pokemon_dict)
    return {"Pokemon añadido": {"Pokemon": pokemon_dict}}
    


@app.put("/pokemons/{pokemon_id}")
def update_pokemon(pokemon_id: int, nuevo_pokemon: Pokemon):
    nuevo_pokemon_dict = nuevo_pokemon.dict()
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            pokemon.update(nuevo_pokemon_dict)
            return{"Éxito": "Pokemon actualizado"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pokémon con ID {pokemon_id} no encontrado"
    )


@app.delete("/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            pokemones.remove(pokemon)
            return{"Éxito": "Pokemon Eliminado"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Pokémon con ID {pokemon_id} no encontrado"
    )
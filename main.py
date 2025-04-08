from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
    return {"error": "No se encontró el pokemon"}

@app.post("/pokemons/")
def create_pokemon(pokemon: Pokemon):
    pokemon_dict = pokemon.dict()
    if pokemon_dict not in pokemones:
        pokemones.append(pokemon_dict)
        return {"Pokemon añadido": {"Pokemon": pokemon_dict}}
    return{"error": "pokemon ya existe"}


@app.put("/pokemons/{pokemon_id}")
def update_pokemon(pokemon_id: int, nuevo_pokemon: Pokemon):
    nuevo_pokemon_dict = nuevo_pokemon.dict()
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            pokemon.update(nuevo_pokemon_dict)
            return{"Éxito": "Pokemon actualizado"}
    return{"Error": "Pokemon no existe"}


@app.delete("/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    for pokemon in pokemones:
        if pokemon["id"] == pokemon_id:
            pokemones.remove(pokemon)
            return{"Éxito": "Pokemon Eliminado"}
    return{"Error": "Pokemon no existe"}
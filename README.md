# PruebaFastAPI
● Instrucciones para ejecutarlo localmente.
Crear ambiente virtual de python: python -m venv env
Ejectuar el ambiente virtual: env\Scripts\activate
Instalar fastAPI: pip install "fastapi[standard]"
Correr la API: fastapi dev main.py
● Explicación de los endpoints.
  -GET/pokemons/     ->  Se obtienen todos los pokemones dentro de la base de datos
  -GET/pokemons/{pokemon_id}    -> Se obtiene el pokemon específico por ID. ID es un entero mayor a 0
  -POST/pokemons/            -> Se añade un nuevo pokemon. Añadir un pokemon con ID ya existente arroja error. ID es un entero mayor a 0
  -PUT/pokemons/{pokemon_id}  -> Se actualiza un nuevo pokemon. No se puede cambiar la ID. ID es un entero mayor a 0
  -DELETE/pokemons/{pokemon_id} -> Se elimina un pokemon por ID. ID es un entero mayor a 0
● Enlace al despliegue en la nube.
https://pokeapi-uv.onrender.com/
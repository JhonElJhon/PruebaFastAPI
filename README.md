# PruebaFastAPI
● Instrucciones para ejecutarlo localmente.
Crear ambiente virtual de python: python -m venv env
Ejectuar el ambiente virtual: env\Scripts\activate
Instalar fastAPI: pip install "fastapi[standard]"
Correr la API: fastapi dev main.py
● Explicación de los endpoints.
REGLAS QUE SIGUEN LOS ENDPOINTS:
Todos los datos numéricos son enteros
Ningún Pokemon puede tener ID menor a 0
Ningún Pokemon puede tener vida menor a 1
Ningún Pokemon puede tener daño o defensa menor a 0
  -GET/pokemons/     ->  Se obtienen todos los pokemones dentro de la base de datos
  -GET/pokemons/{pokemon_id}    -> Se obtiene el pokemon específico por ID.
  -POST/pokemons/            -> Se añade un nuevo pokemon. Añadir un pokemon con ID ya existente arroja error. 
  -PUT/pokemons/{pokemon_id}  -> Se actualiza un nuevo pokemon. No se puede cambiar la ID.
  -DELETE/pokemons/{pokemon_id} -> Se elimina un pokemon por ID.
● Enlace al despliegue en la nube.
https://pokeapi-uv.onrender.com/
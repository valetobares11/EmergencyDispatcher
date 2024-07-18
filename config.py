import os
# get the user name actual
userName = os.getlogin()

# BD
HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
DATABASE = "tesis_bomberos"

# CONFIG
STARTING_POINT = "-64.3451616313023,-33.12684997058952"

CIUDAD = "rio cuarto"
PROVINCIA = "cordoba"
PATH_REPORT = f"/home/{userName}/Descargas/reporte"


PATH_RUTA_EXPORT = f"/home/{userName}/Descargas/file.ods"

# OPERATORS
OPERATORS = [
    'Pedro',
    'Jose',
    'Ignacio'
]


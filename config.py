import os
# BD
HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
DATABASE = "tesis_bomberos"

# Obtén el nombre de usuario actual
nombre_usuario = os.getlogin()

# CONFIG
STARTING_POINT = "-64.3451616313023,-33.12684997058952"

CIUDAD = "rio cuarto"
PROVINCIA = "cordoba"
PATH_REPORTE = f"/home/{nombre_usuario}/Descargas/reporte.txt"
PATH_IMAGEN_CUARTEL_ICON_SVG = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/icon2.svg"
PATH_IMAGEN_BOMBAS_ICON_SVG = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/icon3.svg"
SONIDO_ALARMA_INCENDIO_FORESTAL = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/iforestal.mp3"
SONIDO_ALARMA_INCENDIO_RURAL = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/irural.mp3"
SONIDO_ALARMA_INCENDIO_VEHICULAR = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/ivehicular.mp3"
SONIDO_ALARMA_RESCATE_ESTRUCTURA = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/iestructura.mp3"
SONIDO_ALARMA_ACCIDENTE_VEHICULAR = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/avehicular.mp3"
SONIDO_ALARMA_ACCIDENTE_MAT_PEL= f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/matpel.mp3"
SONIDO_ALARMA_EMERGENCIAS_VARIAS = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/ivarios.mp3"
SONIDO_ALARMA_RESCATE_DE_ALTURA = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/raltura.mp3"
TYPE0 = "DESCONOCIDO"
TYPE1 = "INCENDIO FORESTAL"
TYPE2 = "INCENDIO RURAL"
TYPE3 = "INCENDIO VEHICULAR"
TYPE4 = "INCENDIO ESTRUCTURAL"
TYPE5 = "ACCIDENTE"
TYPE6 = "MATERIAL PELIGROSO"
TYPE7 = "VARIOS"
TYPE8 = "RESCATE DE ALTURA"

# TYPE AUTOMOVILES
TRUCK = "Camioneta"
LIGHT_TRUCK = "Camion ligero"
HEAVY_TRUCK = "Camion pesado"


PATH_RUTA_EXPORT = f"/home/{nombre_usuario}/Descargas/archivo.ods"

# Tipos servicio
TYPE_SERVICIO_HERE_V8 = 7

# OPERATORS
OPERATORS = [
    'Pedro',
    'Jose',
    'Ignacio'
]

# types Emergencia
TYPES_EMERGENCIA = [
    'Todos',
    'Incendio forestal',
    'Incendio rural',
    'Incendio vehicular',
    'Incendio estructural',
    'Accidente',
    'Material peligroso',
    'Rescate altura',
    'Varios'
]

FILTRAR_EMERGENCIA = 0
GRAFICOS_BARRA = 1
GRAFICOS_LINEA = 2
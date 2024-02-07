import os
# BD
HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
DATABASE = "tesis_bomberos"

# Obtén el nombre de usuario actual
nombre_usuario = os.getlogin()

# CONFIG
PUNTO_PARTIDA = "-64.3451616313023,-33.12684997058952"
CIUDAD = "rio cuarto"
PROVINCIA="cordoba"
PATH_REPORTE = f"/home/{nombre_usuario}/Descargas/reporte.txt"
SONIDO_ALARMA_INCENDIO_FORESTAL = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/iforestal.mp3"
SONIDO_ALARMA_INCENDIO_RURAL = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/irural.mp3"
SONIDO_ALARMA_INCENDIO_VEHICULAR = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/ivehicular.mp3"
SONIDO_ALARMA_RESCATE_ESTRUCTURA = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/iestructura.mp3"
SONIDO_ALARMA_ACCIDENTE_VEHICULAR = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/avehicular.mp3"
SONIDO_ALARMA_ACCIDENTE_MAT_PEL= f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/matpel.mp3"
SONIDO_ALARMA_EMERGENCIAS_VARIAS = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/ivarios.mp3"
SONIDO_ALARMA_RESCATE_DE_ALTURA = f"/home/{nombre_usuario}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/OnlineRoutingMapper/sonidos/raltura.mp3"


# TIPO AUTOMOVILES
CAMIONETA = "Camioneta"
CAMION_LIGERO = "Camion ligero"
CAMION_PESADO = "Camion pesado"


PATH_RUTA_EXPORT = "/home/tobares/Descargas/archivo.ods"
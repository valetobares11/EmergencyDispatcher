import os
userName = os.getlogin()


PATH_IMAGEN_CUARTEL_ICON_SVG = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/icon2.svg"
PATH_IMAGEN_BOMBAS_ICON_SVG = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/icon3.svg"
SONIDO_ALARMA_INCENDIO_FORESTAL = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/iforestal.mp3"
SONIDO_ALARMA_INCENDIO_RURAL = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/irural.mp3"
SONIDO_ALARMA_INCENDIO_VEHICULAR = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/ivehicular.mp3"
SONIDO_ALARMA_RESCATE_ESTRUCTURA = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/iestructura.mp3"
SONIDO_ALARMA_ACCIDENTE_VEHICULAR = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/avehicular.mp3"
SONIDO_ALARMA_ACCIDENTE_MAT_PEL= f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/matpel.mp3"
SONIDO_ALARMA_EMERGENCIAS_VARIAS = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/ivarios.mp3"
SONIDO_ALARMA_RESCATE_DE_ALTURA = f"/home/{userName}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DispatcherEmergency/sonidos/raltura.mp3"
TYPE0 = "DESCONOCIDO"
TYPE1 = "INCENDIO FORESTAL"
TYPE2 = "INCENDIO RURAL"
TYPE3 = "INCENDIO VEHICULAR"
TYPE4 = "INCENDIO ESTRUCTURAL"
TYPE5 = "ACCIDENTE"
TYPE6 = "MATERIAL PELIGROSO"
TYPE7 = "VARIOS"
TYPE8 = "RESCATE DE ALTURA"

INCENDIO_FORESTAL=1
INCENDIO_RURAL=2
INCENDIO_VEHICULAR=3
INCENDIO_ESTRUCTURAL=4

# TYPE AUTOMOVILES
TRUCK = "Camioneta"
LIGHT_TRUCK = "Camion ligero"
HEAVY_TRUCK = "Camion pesado"


# Tipos servicio
TYPE_SERVICIO_HERE_V8 = 7


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
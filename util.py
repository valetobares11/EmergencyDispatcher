
from os import close
import requests
from .db import insert,select
from uu import decode
from urllib.request import urlopen
import json
import re
from .config import *
from .db import *
import pandas as pd
from pyexcel_ods import get_data
import psycopg2
from psycopg2 import sql
import pyexcel as pe
from datetime import datetime


from .apikey import *


def geocode_address(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extrae las coordenadas (latitud y longitud) del primer resultado
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lon, lat
    return None

def report(url):
    response = urlopen(url).read().decode("utf-8")
    diccionario = json.loads(response)
    f = open (PATH_REPORTE,'a')
    for route in diccionario['response']['route']:
        f.write(re.sub(r"\<[^>]*\>", "",(route['summary']['text']))+'\n\n')
        for leg in route['leg']:
            for maneuver in leg['maneuver']:
                f.write(re.sub(r"\<[^>]*\>", "",(maneuver['instruction']))+'\n')
    registros = select('points')
    if (len(registros) > 0) :
        f.write('\nCortes\n')
        for x in range(0,len(registros),2):
            f.write(str(registros[x][3]))
    f.close()

def obtener_direccion(latitud, longitud):
    url = f"https://nominatim.openstreetmap.org/search?format=json&lat={latitud}&lon={longitud}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            direccion = data[0]["display_name"]
            return direccion
        else:
            return "No se encontró ninguna dirección para las coordenadas proporcionadas."
    else:
        return f"Error al realizar la solicitud: {response.status_code}"
    
def agregar_texto_con_saltos_de_linea(c, x, y, texto):
    lineas = texto.split('\n')
    for linea in lineas:
        c.drawString(x, y, linea)
        y -= 15  # Espacio vertical entre líneas


def insertar_punto(start_point, stop_point, description):
    valores = "{}, {}, '{}'".format(start_point, stop_point, description)
    insert('points', 'startPoint, stopPoint, description', valores)


def obtener_coordenada(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    
    params = {
        "address": address,
        "key": APIKEY,
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extrae las coordenadas (latitud y longitud) del primer resultado
            lat = float(data["results"][0]["geometry"]["location"]["lat"])
            lon = float(data["results"][0]["geometry"]["location"]["lng"])
            return lon, lat
    return None

def cargar_pedidos(archivo_ods):
    try:
        # Lee el archivo ODS
        data = get_data(archivo_ods)
        
        # Extrae los datos de la primera hoja del archivo ODS
        sheet_name = list(data.keys())[0]
        datos = data[sheet_name]
        
        # Convierte la lista de listas en un DataFrame
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df_filtrado = df.dropna()
        conexion = connectBD()
        cursor = conexion.cursor()
        direccion =''
        startpoint= ''
        stoppoint = ''
        tiempo = ''
        consulta_insercion = ''
        
        for i, fila in df_filtrado.iterrows():
            for columna, valor in fila.items():
                if (columna == 'startpoint'): startpoint = valor
                if (columna == 'stoppoint'): stoppoint = valor
                if (columna == 'direccion'): direccion = valor
                if (columna == 'tiempo'): tiempo = valor
            x,y = obtener_coordenada(direccion+' rio cuarto cordoba')
            stoppoint = '{},{}'.format(x,y)
            consulta_insercion += ("INSERT INTO pedido (direccion, startpoint, stoppoint, tiempo) VALUES ('{}', '{}', '{}', CURRENT_DATE + INTERVAL '{}' HOUR TO MINUTE); \n".format(direccion, startpoint, stoppoint,tiempo))

        cursor.execute(consulta_insercion)
        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()

    except FileNotFoundError:
        print(f"El archivo {archivo_ods} no fue encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo {archivo_ods}: {str(e)}")

def create_and_download_ods():
    data = [
        ["direccion", "solicitante", "telefono", "operador", "startpoint", "stoppoint", "descripcion", "tiempo"]
    ]
    registros = select("pedido")
    for tupla in registros:
        data.append([tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7],tupla[8].strftime("%Y-%m-%d %H:%M:%S")])

    # Crear un libro de trabajo con pyexcel
    sheet = pe.Sheet(data)

    # Guardar el libro de trabajo como un archivo ODS
    sheet.save_as(PATH_RUTA_EXPORT)
    
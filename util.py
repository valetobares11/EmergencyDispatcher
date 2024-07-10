
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

def escribir_instrucciones(diccionario, archivo, titulo):
    archivo.write(titulo + '\n')
    instrucciones = diccionario['routes'][0]['sections'][0]['actions']
    for instruccion in instrucciones:
        archivo.write(str(instruccion['instruction']) + '\n')

def obtener_datos_url(url):
    response = urlopen(url).read().decode("utf-8")
    return json.loads(response)

def report(urlIda, urlVuelta):
    diccionario_ida = obtener_datos_url(urlIda)
    diccionario_vuelta = obtener_datos_url(urlVuelta)
    with open(PATH_REPORTE, 'a') as f:

        estimatedTime = int(diccionario_ida['routes'][0]['sections'][0]['summary']['duration'])
        f.write('El tiempo estimado de viaje es: '+ str(round(estimatedTime/60))+' min\n\n')
        
        escribir_instrucciones(diccionario_ida, f, 'Detalle de ruta de ida:')
        f.write('\n\n')
        escribir_instrucciones(diccionario_vuelta, f, 'Detalle de ruta de vuelta:')

        registros = select('points')
        if (len(registros) > 0) :
            f.write('\nCortes\n')
            for x in range(0,len(registros),2):
                f.write(str(registros[x][3]))
        f.close()

def writeReport(description, address, applicant, phone):
    f = open (PATH_REPORTE ,'w')
    f.write('Descripcion Emergencia: '+description)
    f.write('\n\nDireccion: '+address)
    f.write('\n\nSolicitante: '+applicant)
    f.write('\n\nTelefono: '+phone+'\n\n')
    f.close()

def getAddress(longitud, latitud):
    url = f" https://maps.googleapis.com/maps/api/geocode/json?latlng={latitud},{longitud}&key={APIKEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            direccion = data['results'][0]['formatted_address']
            return direccion
        else:
            return "No se encontró ninguna dirección para las coordenadas proporcionadas."
    else:
        return f"Error al realizar la solicitud: {response.status_code}"

def insertPoint(start_point, stop_point, description):
    valores = "{}, {}, '{}'".format(start_point, stop_point, description)
    insert('points', 'startPoint, stopPoint, description', valores)


def getCoordinate(address):
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

def loadOrders(archivo_ods):
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
            for column, valor in fila.items():
                if (column == 'startpoint'): startpoint = valor
                if (column == 'stoppoint'): stoppoint = valor
                if (column == 'direccion'): direccion = valor
                if (column == 'tiempo'): tiempo = valor
            x,y = obtener_coordenada(direccion+' rio cuarto cordoba')
            stoppoint = '{},{}'.format(x,y)
            consulta_insercion += ("INSERT INTO order (direccion, startpoint, stoppoint, tiempo) VALUES ('{}', '{}', '{}', CURRENT_DATE + INTERVAL '{}' HOUR TO MINUTE); \n".format(direccion, startpoint, stoppoint,tiempo))

        cursor.execute(consulta_insercion)
        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()

    except FileNotFoundError:
        print(f"El archivo {archivo_ods} no fue encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo {archivo_ods}: {str(e)}")

def createAndDownloadOds():
    data = [
        ["direccion", "applicant", "phone", "operador", "startpoint", "stoppoint", "description", "tiempo"]
    ]
    registros = select("order")
    for tupla in registros:
        data.append([tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7],tupla[8].strftime("%Y-%m-%d %H:%M:%S")])

    # Crear un libro de trabajo con pyexcel
    sheet = pe.Sheet(data)

    # Guardar el libro de trabajo como un archivo ODS
    sheet.save_as(PATH_RUTA_EXPORT)
    
def getIdTypeEmergency(emergency):
    if (emergency == 'Incendio forestal'):
        return "INCENDIO FORESTAL"
    if (emergency == 'Incendio rural'):
        return "INCENDIO RURAL"
    if (emergency == 'Incendio vehicular'):
        return "INCENDIO VEHICULAR"
    if (emergency == 'Incendio estructural'):
        return "INCENDIO ESTRUCTURAL"
    if (emergency == 'Accidente'):
        return "ACCIDENTE"
    if (emergency == 'Material peligroso'):
        return "MATERIAL PELIGROSO"
    if (emergency == 'Varios'):
        return "VARIOS"
    if (emergency == 'Rescate altura'):
        return "RESCATE DE ALTURA"
    
    return "DESCONOCIDO"

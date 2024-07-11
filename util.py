
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


def geocodeAddress(address):
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

def writeInstructions(diccionario, file, title):
    file.write(title + '\n')
    instructions = diccionario['routes'][0]['sections'][0]['actions']
    for instruction in instructions:
        file.write(str(instruction['instruction']) + '\n')

def getDataUrl(url):
    response = urlopen(url).read().decode("utf-8")
    return json.loads(response)

def report(urlIda, urlVuelta):
    dictionary1 = getDataUrl(urlIda)
    dictionary2 = getDataUrl(urlVuelta)
    with open(PATH_REPORTE, 'a') as f:

        estimatedTime = int(dictionary1['routes'][0]['sections'][0]['summary']['duration'])
        f.write('El time estimado de viaje es: '+ str(round(estimatedTime/60))+' min\n\n')
        
        writeInstructions(dictionary1, f, 'Detalle de ruta de ida:')
        f.write('\n\n')
        writeInstructions(dictionary2, f, 'Detalle de ruta de vuelta:')

        records = select('points')
        if (len(records) > 0) :
            f.write('\nCortes\n')
            for x in range(0,len(records),2):
                f.write(str(records[x][3]))
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
            address = data['results'][0]['formatted_address']
            return address
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

def loadOrders(fileOds):
    try:
        # Lee el file ODS
        data = get_data(fileOds)
        
        # Extrae los datos de la primera hoja del file ODS
        sheet_name = list(data.keys())[0]
        datos = data[sheet_name]
        
        # Convierte la lista de listas en un DataFrame
        df = pd.DataFrame(datos[1:], columns=datos[0])
        df_filtrado = df.dropna()
        conexion = connectBD()
        cursor = conexion.cursor()
        address =''
        startpoint= ''
        stoppoint = ''
        actual_time = 0
        applicant=''
        operator = ''
        phone=''
        description=''
        type=''
        estimatedTime=0
        queryInsertion = ''
        
        for i, fila in df_filtrado.iterrows():
            for column, valor in fila.items():
                if (valor!=''):
                    if (column == 'startpoint'): startpoint = valor
                    if (column == 'stoppoint'): stoppoint = valor
                    if (column == 'direccion'): address = valor
                    if (column == 'tiempo'): actual_time = valor
                    if (column == 'operador'): operator = valor
                    if (column == 'solicitante'): applicant = valor
                    if (column == 'telefono'): phone = valor
                    if (column == 'decripcion'): description = valor
                    if (column == 'tipo'): type = valor
                    if (column == 'tiempo_estimado'):estimatedTime = valor

            x,y = getCoordinate(address+' rio cuarto cordoba')
            stoppoint = '{},{}'.format(x,y)
            queryInsertion += ("INSERT INTO orders (address,applicant, phone, operator, startpoint, stoppoint,description,estimated_time,type, actual_time) VALUES ('{}','{}','{}', '{}', '{}','{}','{}','{}','{}','{}'); \n".format(address,applicant,phone, operator,startpoint,stoppoint,description,estimatedTime,type,actual_time))
        cursor.execute(queryInsertion)
        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()

    except FileNotFoundError:
        print(f"El file {fileOds} no fue encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo {fileOds}: {str(e)}")

def createAndDownloadOds():
    data = [
        ["direccion", "solicitante", "telefono", "operador", "startpoint", "stoppoint", "descripcion", "tiempo_estimado","tipo", "tiempo_real", "fecha"]
    ]
    registros = select("orders")
    for tupla in registros:
        data.append([tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7],tupla[8],tupla[10],tupla[11],tupla[12].strftime("%Y-%m-%d %H:%M:%S")])

    # Crear un libro de trabajo con pyexcel
    sheet = pe.Sheet(data)

    # Guardar el libro de trabajo como un file ODS
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

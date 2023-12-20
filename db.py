import psycopg2
from psycopg2 import sql
from .config import *
                
def connectBD():
    # Conectar a la base de datos
    conexion = psycopg2.connect(
        host = HOST,
        user = USER,
        password = PASSWORD,
        database = DATABASE
    )
    return conexion

def createTablePoints():
    conexion = connectBD()
    cursor = conexion.cursor()

    # Crear una tabla si no existe
    consulta_creacion_tabla = """
        CREATE TABLE IF NOT EXISTS points (
            id SERIAL PRIMARY KEY,
            startPoints VARCHAR(40),
            stopPoints VARCHAR(40),
            description VARCHAR(255)
        )
    """
    cursor.execute(consulta_creacion_tabla)

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def insertarPoints(startPoint,stopPoint, descripicon=""):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_insercion_point = sql.SQL("INSERT INTO points (startPoints, stopPoints, description) VALUES (%s, %s, %s)")
    datos_point = (startPoint, stopPoint, descripicon)
    cursor.execute(consulta_insercion_point, datos_point)


    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def seleccionarPoints():
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_point = "SELECT * FROM points"

    cursor.execute(consulta_seleccion_point)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados

def seleccionarPoint(id):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_point = "SELECT * FROM points WHERE id = {}".format(id)

    cursor.execute(consulta_seleccion_point)

    resultado = cursor.fetchall()
    conexion.close()
    
    return resultado[0]

def borrarPoint(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    consulta_delete_point = sql.SQL("DELETE FROM points WHERE id = {}".format(id))
    cursor.execute(consulta_delete_point)
    conexion.commit()
    conexion.close()

#tabla para tener registro de las bombas de aguas que pueden ser utilizadas en un incendio
def createTableBomba():
    conexion = connectBD()
    cursor = conexion.cursor()

    # Crear una tabla si no existe
    consulta_creacion_tabla_bomba = """
        CREATE TABLE IF NOT EXISTS bomba (
            id SERIAL PRIMARY KEY,
            startPoints VARCHAR(40),
            stopPoints VARCHAR(40),
            description VARCHAR(255)
        )
    """
    cursor.execute(consulta_creacion_tabla)

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def insertarPoints(startPoint,stopPoint, descripicon=""):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_insercion_bomba = sql.SQL("INSERT INTO bomba (startPoints, stopPoints, description) VALUES (%s, %s, %s)")
    datos_point = (startPoint, stopPoint, descripicon)
    cursor.execute(consulta_insercion_bomba, datos_point)


    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def seleccionarBomba():
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_point = "SELECT * FROM bomba"

    cursor.execute(consulta_seleccion_bomba)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados

def seleccionarBomba(id):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_bomba = "SELECT * FROM bomba WHERE id = {}".format(id)

    cursor.execute(consulta_seleccion_bomba)

    resultado = cursor.fetchall()
    conexion.close()
    
    return resultado[0]

def borrarPoint(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    consulta_delete_bomba = sql.SQL("DELETE FROM bomba WHERE id = {}".format(id))
    cursor.execute(consulta_delete_bomba)
    conexion.commit()
    conexion.close()

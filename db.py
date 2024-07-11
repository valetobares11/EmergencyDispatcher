import psycopg2
from psycopg2 import sql
from .config import *
import datetime
                
def connectBD():
    # Conectar a la base de datos
    conexion = psycopg2.connect(
        host = HOST,
        user = USER,
        password = PASSWORD,
        database = DATABASE
    )
    return conexion

def createTablePoint():
    conexion = connectBD()
    cursor = conexion.cursor()

    # Crear una tabla si no existe
    queryCreation = """
        CREATE TABLE IF NOT EXISTS points (
            id SERIAL PRIMARY KEY,
            startPoint VARCHAR(40),
            stopPoint VARCHAR(40),
            description VARCHAR(255)
        )
    """
    cursor.execute(queryCreation)

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def insert(table = '', columns = '', values = ''):
    if table != '' and columns != '' and values != '':
        conexion = connectBD()
        cursor = conexion.cursor()
        consulta_insercion = sql.SQL("INSERT INTO {} ({}) VALUES ({})".format(table, columns, values))
        cursor.execute(consulta_insercion)

        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()

def insertOrder(address, applicant, phone, operator, startpoint, stoppoint, description, estimatedTime, type):
    conexion = connectBD()
    cursor = conexion.cursor()
    
    queryInsertionOrder = sql.SQL("INSERT INTO orders (address, applicant, phone, operator, startpoint, stoppoint, description, estimated_time, type,actual_time,date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())")
    datosOrder = (address, applicant, phone, operator, startpoint, stoppoint, description, estimatedTime, type,0)
    cursor.execute(queryInsertionOrder, datosOrder)


    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def select(table = '', id = None, limit = None, filtro = {}):
    if (table == ''):
        return []
    
    conexion = connectBD()
    cursor = conexion.cursor()
    query = "SELECT * FROM {} WHERE 1 = 1 ".format(table)
    
    if (id is not None):
        query+= " AND id = {} ".format(id)

    if 'fecha_desde' in filtro:
        query += " AND date >= '{}'".format(filtro['fecha_desde'])

    if 'fecha_hasta' in filtro:
        query += " AND date <= '{}'".format(filtro['fecha_hasta'])

    if 'type_emergency' in filtro:
        query += " AND type = '{}'".format(filtro['type_emergency'])
    
    if 'hours' in filtro:
        query+= " AND EXTRACT(HOUR FROM date) = '{}'".format(filtro['hours'])

    query += "ORDER BY id"

    if (limit is not None):
        query+= " DESC LIMIT {}".format(limit)
    
    cursor.execute(query)
    result = cursor.fetchall()
    conexion.close()

    return result[0] if id is not None else result

def delete(table = '', id = None):
    if (table != ''):
        conexion = connectBD()
        cursor = conexion.cursor()
        query = "DELETE FROM {} WHERE 1 = 1".format(table)
        
        if (id is not None):
            query+= " AND id = {}".format(id)
        
        cursor.execute(sql.SQL(query))
        conexion.commit()
        conexion.close()

def update(table = '', seters = '', id = None):
    if (table != '' and seters != ''):
        conexion = connectBD()
        cursor = conexion.cursor()
        query = "UPDATE {} SET {} WHERE 1 = 1 AND id = {} ;".format(table ,seters,id)
        cursor.execute(sql.SQL(query))
        conexion.commit()
        conexion.close()

# def update_file(table = '',nombre='', contenido = '', id = None):
#     if (table != '' and contenido != ''):
#         conexion = connectBD()
#         cursor = conexion.cursor()
        
#         # Prepara la consulta SQL con un parámetro para el contenido binario
#         query = sql.SQL("UPDATE archivo SET nombre_archivo = %s, contenido = %s WHERE id = %s")
    
#         # Ejecuta la consulta SQL pasando los datos binarios como parámetros
#         cursor.execute(query, (nombre, psycopg2.Binary(contenido), id))
        
#         conexion.commit()
#         conexion.close()




#tabla para tener registro de las pumps de aguas que pueden ser utilizadas en un incendio
def createTablePump():
    conexion = connectBD()
    cursor = conexion.cursor()

    # Crear una tabla si no existe
    queryCreation = """
        CREATE TABLE IF NOT EXISTS pump (
            id SERIAL PRIMARY KEY,
            startPoint VARCHAR(40),
            stopPoint VARCHAR(40),
            description VARCHAR(255),
            state CHAR(1) CHECK (state IN ('I', 'A')) DEFAULT 'A'
        )
    """
    cursor.execute(queryCreation)

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def insertPump(startPoint,stopPoint, description=""):
    conexion = connectBD()
    cursor = conexion.cursor()

    queryInsertPump = sql.SQL("INSERT INTO pump (startpoint, stoppoint, description) VALUES (%s, %s, %s)")
    datosPump = (startPoint, stopPoint, description)
    cursor.execute(queryInsertPump, datosPump)


    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def selectPump():
    conexion = connectBD()
    cursor = conexion.cursor()

    querySelectPump = "SELECT * FROM pump"

    cursor.execute(querySelectPump)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados

def selectPump(id):
    conexion = connectBD()
    cursor = conexion.cursor()

    querySelectPump = "SELECT * FROM pump WHERE id = {}".format(id)

    cursor.execute(querySelectPump)

    resultado = cursor.fetchall()
    conexion.close()
    
    return resultado[0]

def deletePump(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    queryDeletePump = sql.SQL("DELETE FROM pump WHERE id = {}".format(id))
    cursor.execute(queryDeletePump)
    conexion.commit()
    conexion.close()

def createTableOrder():
    conexion = connectBD()
    cursor = conexion.cursor()

    # Crear una tabla si no existe
    queryCreationTable = """
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            name TEXT,
            content BYTEA
        );

        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            address VARCHAR(100),
            applicant VARCHAR(40),
            phone VARCHAR(40),
            operator VARCHAR(40),
            startpoint VARCHAR(100),
            stoppoint VARCHAR(100),
            description VARCHAR(255),
            estimated_time INT,
            id_file INT,
            type VARCHAR(40),
            actual_time INT,
            date TIMESTAMP,
            FOREIGN KEY (id_file) REFERENCES files(id)
        );
    """
    cursor.execute(queryCreationTable)

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()




def selectOrder():
    conexion = connectBD()
    cursor = conexion.cursor()

    querySelectOrders = "SELECT * FROM orders"

    cursor.execute(querySelectOrders)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados

def selectOrder(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    querySelectOrders = "SELECT * FROM orders WHERE id = {}".format(id)
    cursor.execute(querySelectOrders)
    resultado = cursor.fetchall()
    conexion.close()
    
    return resultado[0]

def deleteOrder(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    queryDeleteOrder = sql.SQL("DELETE FROM orders WHERE id = {}".format(id))
    cursor.execute(queryDeleteOrder)
    conexion.commit()
    conexion.close()


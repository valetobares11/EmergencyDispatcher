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


def select(table = '', id = None, limit = None, filtro = {}):
    if (table == ''):
        return []
    
    conexion = connectBD()
    cursor = conexion.cursor()
    query = "SELECT * FROM {} WHERE 1 = 1 ".format(table)
    
    if (id is not None):
        query+= " AND id = {} ".format(id)

    if 'fecha_desde' in filtro:
        query += " AND fecha >= '{}'".format(filtro['fecha_desde'])

    if 'fecha_hasta' in filtro:
        query += " AND fecha <= '{}'".format(filtro['fecha_hasta'])

    if 'type_emergency' in filtro:
        query += " AND type = '{}'".format(filtro['type_emergency'])
    
    if 'hours' in filtro:
        query+= " AND EXTRACT(HOUR FROM fecha) = '{}'".format(filtro['hours'])

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
        query = "UPDATE {} SET {} WHERE 1 = 1 AND id = {} ;".format(table,seters,id)

        cursor.execute(sql.SQL(query))
        conexion.commit()
        conexion.close()

def update_file(table = '',nombre='', contenido = '', id = None):
    if (table != '' and contenido != ''):
        conexion = connectBD()
        cursor = conexion.cursor()
        
        # Prepara la consulta SQL con un parámetro para el contenido binario
        query = sql.SQL("UPDATE archivo SET nombre_archivo = %s, contenido = %s WHERE id = %s")
    
        # Ejecuta la consulta SQL pasando los datos binarios como parámetros
        cursor.execute(query, (nombre, psycopg2.Binary(contenido), id))
        
        conexion.commit()
        conexion.close()




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


def insertarBomba(startPoint,stopPoint, description=""):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_insercion_pump = sql.SQL("INSERT INTO pump (startpoint, stoppoint, description) VALUES (%s, %s, %s)")
    datos_pump = (startPoint, stopPoint, description)
    cursor.execute(consulta_insercion_pump, datos_pump)


    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def seleccionarBomba():
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_pump = "SELECT * FROM pump"

    cursor.execute(consulta_seleccion_pump)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados

def seleccionarBomba(id):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_pump = "SELECT * FROM pump WHERE id = {}".format(id)

    cursor.execute(consulta_seleccion_pump)

    resultado = cursor.fetchall()
    conexion.close()
    
    return resultado[0]

def borrarBomba(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    consulta_delete_pump = sql.SQL("DELETE FROM pump WHERE id = {}".format(id))
    cursor.execute(consulta_delete_pump)
    conexion.commit()
    conexion.close()

def createTableOrder():
    conexion = connectBD()
    cursor = conexion.cursor()

    # Crear una tabla si no existe
    consulta_creacion_tabla_order = """
        CREATE TABLE IF NOT EXISTS file (
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
            estimatedTime INT,
            idFile INT,
            type VARCHAR(40),
            actualTime INT,
            fecha TIMESTAMP,
            FOREIGN KEY (idFile) REFERENCES archivo(id)
        );
    """
    cursor.execute(consulta_creacion_tabla_order)

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def insertarPedido(address, applicant, phone, operator, startpoint, stoppoint, description, estimatedTime, type):
    conexion = connectBD()
    cursor = conexion.cursor()
    
    consulta_insercion_order = sql.SQL("INSERT INTO orders (address, applicant, phone, operator, startpoint, stoppoint, description, estimatedTime, type,actualTime,fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())")
    datos_order = (address, applicant, phone, operator, startpoint, stoppoint, description, estimatedTime, type,0)
    cursor.execute(consulta_insercion_order, datos_order)


    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()


def seleccionarPedido():
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_order = "SELECT * FROM orders"

    cursor.execute(consulta_seleccion_order)

    resultados = cursor.fetchall()
    conexion.close()

    return resultados

def seleccionarPedido(id):
    conexion = connectBD()
    cursor = conexion.cursor()

    consulta_seleccion_order = "SELECT * FROM orders WHERE id = {}".format(id)

    cursor.execute(consulta_seleccion_order)

    resultado = cursor.fetchall()
    conexion.close()
    
    return resultado[0]

def borrarPedido(id):
    conexion = connectBD()
    cursor = conexion.cursor()
    consulta_delete_order = sql.SQL("DELETE FROM orders WHERE id = {}".format(id))
    cursor.execute(consulta_delete_order)
    conexion.commit()
    conexion.close()


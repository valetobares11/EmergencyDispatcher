
import requests

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


def agregar_texto_con_saltos_de_linea(c, x, y, texto):
    lineas = texto.split('\n')
    for linea in lineas:
        c.drawString(x, y, linea)
        y -= 15  # Espacio vertical entre líneas


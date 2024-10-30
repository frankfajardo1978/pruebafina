from fastapi import FastAPI
import pandas as pd
from datetime import datetime

# Inicializar la aplicación FastAPI
app = FastAPI()

# Cargar el archivo CSV al iniciar la aplicación
data = pd.read_csv("archivotransformado.csv")


@app.get("/")
def read_root():
    return {"Bienvenido       
    para consultar mes se coloca /mes =   y dia /dia"}


@app.get("/mes")
def cantidad_filmaciones_mes(mes: str):
    # Convertir el mes a minúsculas para evitar problemas de mayúsculas
    mes = mes.lower()
    
    # Diccionario para convertir el nombre del mes en español al número correspondiente
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    # Validar si el mes ingresado es válido
    if mes not in meses:
        return {"error": "Mes ingresado no válido. Por favor, ingrese un mes en español."}
    
    # Obtener el número del mes correspondiente
    numero_mes = meses[mes]
    
    # Convertir la columna de fechas al tipo datetime si es necesario
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    
    # Filtrar las películas estrenadas en el mes especificado
    peliculas_mes = data[data['release_date'].dt.month == numero_mes]
    cantidad = len(peliculas_mes)
    
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"}




# Definir el endpoint para cantidad_filmaciones_dia
@app.get("/dia")
def cantidad_filmaciones_dia(dia: str):
    dia = dia.capitalize()  # Ajustar la capitalización para comparación
    cantidad = data[data['dia_semana'] == dia].shape[0]  # Contar películas
    return {"mensaje": f"{cantidad} películas fueron estrenadas en los días {dia}"}


# Diccionario para traducir nombres de días de inglés a español
dias_traduccion = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Convertir la columna de fecha a formato de fecha y extraer el día de la semana en inglés
data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
data['dia_semana'] = data['release_date'].dt.day_name()
data['dia_semana'] = data['dia_semana'].map(dias_traduccion)  # Traducir a español

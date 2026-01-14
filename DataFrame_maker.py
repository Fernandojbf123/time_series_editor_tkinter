import pandas as pd
import numpy as np  
import pickle
import matplotlib.dates as mdates

# Función para crear datos de ejemplo
def create_sample_data(ndays=200):
    """Crea datos de ejemplo con fechas y múltiples columnas de datos"""
    # Crear fechas desde hoy hasta 10 días atrás
    dates = pd.date_range(start='2024-01-01', periods=ndays, freq='h')
    
    # Crear datos aleatorios para las columnas
    np.random.seed(42)
    data_dict = {
        'tspan': dates,
        'temperatura': np.random.randn(ndays) * 5 + 20,
        'humedad': np.random.rand(ndays) * 100,
        'presion': np.random.randn(ndays) * 10 + 1013,
        'luz': np.random.rand(ndays) * 1000,
        'ruido': np.random.rand(ndays) * 70,
        'viento': np.random.rand(ndays) * 30,
        'precipitacion': np.random.rand(ndays) * 10,
        'uv_index': np.random.rand(ndays) * 11,
        'co2': np.random.randn(ndays) * 50 + 400,
        'pm25': np.random.rand(ndays) * 150,
        'pm10': np.random.rand(ndays) * 200,
        'ozono': np.random.rand(ndays) * 300,
        'monoxido_carbono': np.random.rand(ndays) * 10,
        'dioxido_nitrogeno': np.random.rand(ndays) * 200
    }
    return pd.DataFrame(data_dict)

def leer_datos_de_corrientes_pickle(ruta_archivo):
    with open(ruta_archivo, 'rb') as file:
        data = pickle.load(file)
    return data

def crear_dataframe_corrientes_desde_pickle(data):
    tspan = data.index
    rap = data['Rap']
    rap = np.vstack(rap)
    # profs = data['Profundidades'][0]

    df = pd.DataFrame()
    df['tspan'] = tspan
    profs = []
    for prof in range(rap.shape[1]):
        if np.nansum(rap[:, prof]) != 0:
            df[f"rap_{prof}"] = rap[:, prof]
            profs.append(prof)

    prof = profs.copy()

    df["Temp_ADCP"] = data['Temp'].to_numpy()
    df["Dir"] = data['Dir'].to_numpy()
    df["Temperatura_MCT"] = data['Temperatura del agua (MCT)'].to_numpy()
    df["Conductividad_MCT"] = data['Conductividad'].to_numpy()
    df["Salinidad_MCT"] = data['Salinidad'].to_numpy()


    return df, prof




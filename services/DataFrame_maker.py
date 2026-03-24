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



def crear_dataframe_corrientes_desde_pickle(data,):
    data.index = pd.to_datetime(data.index)
    if "Fecha y hora de medicion" in data.columns:
        data.set_index("Fecha y hora de medicion", inplace=True)
    tspan = data.index
    
    rap = data['Rap']
    rap = np.vstack(rap)
    dir = data['Dir']
    dir = np.vstack(dir)

    df = pd.DataFrame()
    df['tspan'] = tspan
    profs = []
    nivel = 1
    for prof in range(rap.shape[1]):
        if np.nansum(rap[:, prof]) != 0:   
            df[f"rap_{nivel}"] = rap[:, prof]
            df[f"dir_{nivel}"] = dir[:, prof]
            profs.append(prof)
            nivel += 1

    df["temp_adcp"] = data['Temp'].to_numpy()
    if "Temperatura del agua (MCT)" in data.columns:
        df["temperatura_mct"] = data['Temperatura del agua (MCT)'].to_numpy()
    if "Conductividad" in data.columns and "Salinidad" in data.columns:
        df["conductividad_mct"] = data['Conductividad'].to_numpy()
        df["salinidad_mct"] = data['Salinidad'].to_numpy()

    df.sort_values('tspan', inplace=True)
    return df, profs

def crear_dataframe_viento_desde_pickle(data):
    data.index = pd.to_datetime(data.index)
    if "Fecha y hora de medicion" in data.columns:
        data.set_index("Fecha y hora de medicion", inplace=True)
    tspan = data.index
    
    df = pd.DataFrame()
    df['tspan'] = tspan
    df['Pa'] = data['Pa'].to_numpy()
    df['Ta'] = data['Ta'].to_numpy()
    df['HR'] = data['HR'].to_numpy()
    df['Punto de Rocio'] = data['Punto de Rocio'].to_numpy()
    df['Rap2'] = data['Rap2'].to_numpy()
    df['Dir2'] = data['Dir2'].to_numpy()
    df['u (mecanico)'] = data['u (mecanico)'].to_numpy()
    df['v (mecanico)'] = data['v (mecanico)'].to_numpy()
    df['R5s2'] = data['R5s2'].to_numpy()    
    df['R1s2'] = data['R1s2'].to_numpy()
    df['Rap1'] = data['Rap1'].to_numpy()
    df['Dir1'] = data['Dir1'].to_numpy()
    df['u (sonico)'] = data['u (sonico)'].to_numpy()
    df['v (sonico)'] = data['v (sonico)'].to_numpy()
    df['R5s1'] = data['R5s1'].to_numpy()
    df['R1s1'] = data['R1s1'].to_numpy()
    df['Temperatura (sonico)'] = data['Temperatura (sonico)'].to_numpy()
    df['Presion (sonico)'] = data['Presion (sonico)'].to_numpy()
    df['Humedad relativa (sonico)'] = data['Humedad relativa (sonico)'].to_numpy()
    df['Lluvia acumulada'] = data['Lluvia acumulada'].to_numpy()
    df['Duracion de la lluvia'] = data['Duracion de la lluvia'].to_numpy()
    df['Intensidad de la lluvia'] = data['Intensidad de la lluvia'].to_numpy()
    df['Lat'] = data['Lat'].to_numpy()  
    df['Lon'] = data['Lon'].to_numpy()
    
    df.sort_values('tspan', inplace=True)
    return df

def crear_dataframe_oleaje_desde_pickle(data):
    data.index = pd.to_datetime(data.index)
    if "Fecha y hora de medicion" in data.columns:
        data.set_index("Fecha y hora de medicion", inplace=True)
    tspan = data.index
    
    df = pd.DataFrame()
    df['tspan'] = tspan
    df['Hs'] = data['Hs'].to_numpy()
    df['Hmax'] = data['Hm'].to_numpy()
    df['Tp'] = data['Tp'].to_numpy()
    df['dir'] = data['Diro'].to_numpy()
    df['vardir'] = data['VarDir'].to_numpy()
    
    df.sort_values('tspan', inplace=True)
    return df


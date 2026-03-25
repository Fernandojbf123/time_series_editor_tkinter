import os
import pickle
import numpy as np
import pandas as pd
import netCDF4 as nc
from services.date_functions import datenum_to_datetime
from services.get_tspan import get_tspan
from services.DataFrame_maker import *
from services.uv2polar import uv2polar

"""" 
Este archivo contiene las funciones de carga de cada tipo de archivo; cada función devuelve un dataframe.
También contiene la función que unifica los dataframes de diferentes boyas.

"""

########## ADCP ##########
# 1. Cargar CSV de memoria del ADCP
def cargar_memoria_adcp_csv(ruta_a_carpeta:str, nombre_de_archivos:list, fecha_de_inicio:str, fecha_final:str) -> pd.DataFrame:
    """ Carga archivos CSV de la memoria del ADCP y los concatena en un solo DataFrame
    Devuelve un dataframe con las variables relevantes dentro del rango de fechas seleccionado.
    Las fechas serán redondeadas a horas exactas; ejemplo 10:02, o 10:50 se redondeará a 10:00
    """
    
    output_df = pd.DataFrame()
    joined_df = pd.DataFrame()
    for archivo in nombre_de_archivos:
        ruta_archivo = os.path.join(ruta_a_carpeta, archivo)
        dt_tmp = pd.read_csv(ruta_archivo)
        joined_df = pd.concat([joined_df, dt_tmp], axis=0)
    
    cantidad_de_niveles = 0
    for column in joined_df.columns:
        if "DateTime" in column:            
            output_df["tspan"] = pd.to_datetime(joined_df[column], format="%m/%d/%Y %H:%M:%S", errors='coerce')
        elif column == "Temperature":
            output_df["temp_adcp"] = pd.to_numeric(joined_df[column])
        elif "East" in column:
            new_columna_name = column.replace("#","_").replace("East","u")
            output_df[new_columna_name] = pd.to_numeric(joined_df[column])
            cantidad_de_niveles += 1
        elif "North" in column:
            new_columna_name = column.replace("#","_").replace("North","v")
            output_df[new_columna_name] = pd.to_numeric(joined_df[column])
    
    # Filtrar por fecha de inicio y fecha final
    if fecha_de_inicio is not None and fecha_final is not None:
        mask = (output_df['tspan'] >= pd.to_datetime(fecha_de_inicio, format="%d/%m/%Y %H:%M")) & \
               (output_df['tspan'] <= pd.to_datetime(fecha_final, format="%d/%m/%Y %H:%M"))
        output_df = output_df.loc[mask]
        
    output_df.loc[:, "tspan"] = output_df.loc[:, "tspan"].dt.round('h') # Redondear a horas exactas
    output_df = output_df.drop_duplicates(subset="tspan", keep="first").reset_index(drop=True) # Eliminar filas con tspan duplicados, quedándose con la primera ocurrencia
    
    #Cambiar u y v por rap y dir
    for nivel in range(1, cantidad_de_niveles+1):
        u = output_df.pop(f"u_{nivel}")
        v = output_df.pop(f"v_{nivel}")
        dir, rap = uv2polar(u, v)
        output_df.loc[:, f"rap_{nivel}"] = rap
        output_df.loc[:, f"dir_{nivel}"] = dir
    
    return output_df


# 2. Cargar telemetria .dat del ADCP  
def cargar_telemetria_adcp_dat(ruta_a_carpeta, nombre_de_archivo, indices):
    """ Carga un archivo .dat de telemetría del ADCP y devuelve un DataFrame con las variables relevantes"""
    dict_corrientes = {}
    ruta_a_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    with open(ruta_a_archivo, 'r', encoding='utf-8') as archivo:
        # Corrientes
        for linea in archivo:
            tmp_dir = separar_linea_de_dat_txt_corrientes(linea, indices)
            if tmp_dir is not None:
                for key, value in tmp_dir.items():
                    if key not in dict_corrientes:
                        dict_corrientes[key] = []
                    dict_corrientes[key].append(value)
                
    output_df = pd.DataFrame(dict_corrientes)
    output_df.sort_values('tspan', inplace=True)
    output_df.drop_duplicates(subset='tspan', inplace=True, keep='first')
    output_df.reset_index(drop=True, inplace=True)

    return output_df 

# 3. Cargar pickle del ADCP crudo / validado
def cargar_pickle_adcp(ruta_a_carpeta, nombre_de_archivo):
     ruta_de_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
     df_pkl = leer_datos_de_pickle(ruta_de_archivo)
     output_df, prof = crear_dataframe_corrientes_desde_pickle(df_pkl)
     return output_df, prof

# 4. Cargar NETCDF del ADCP
def cargar_nc_adcp(ruta_a_carpeta, nombre_de_archivo):
    """ Carga el NETCDF del ADCP y devuelve un DataFrame con las variables relevantes"""
    ruta_nc = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    dataset = nc.Dataset(ruta_nc)
    
    # Extraer variables relevantes
    jd = np.array(dataset.variables['jd'][:])
    tspan = pd.to_datetime(datenum_to_datetime(jd))
    u = np.array(dataset.variables['u'][:])
    v = np.array(dataset.variables['v'][:])
    dir, rap = uv2polar(u, v)
    
    temp = np.array(dataset.variables['Temp'][:]).flatten()
    
    # Crear un DataFrame
    output_dict = {
        'tspan': tspan,  # Convertir tiempo a formato datetime
        'temp_adcp': temp
    }
    
    
    for inivel in range(1, u.shape[1]+1):
        output_dict[f"rap_{inivel}"] = []
        output_dict[f"dir_{inivel}"] = []
        output_dict[f"rap_{inivel}"] = rap[:, inivel-1]
        output_dict[f"dir_{inivel}"] = dir[:, inivel-1]

    df = pd.DataFrame(output_dict)
    return df


############ OLEAJE ##########
# 1. Cargar crudo unido mem o realt
def cargar_pickle_oleaje(ruta_a_carpeta, nombre_de_archivo):
    """
    unido mem = binario mem + telemetría mem + binario realt + telemetría realt)
    unido realt = binario realt + telemetría realt
    Carga un archivo .pkl de oleaje (binario unido con telemetría 
    """
    ruta_de_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    df_pkl = leer_datos_de_pickle(ruta_de_archivo)
    output_df = crear_dataframe_oleaje_desde_pickle(df_pkl)
    return output_df
 
# 3. Cargar datos de dirspec de memoria (DIRSPEC)

# 4. Cargar datos de dirspec de telemetria (DIRSPEC)

# 5. Cargar NETCDF de oleaje
def cargar_nc_oleaje(ruta_a_carpeta, nombre_de_archivo):
    """ Carga el NETCDF de oleaje y devuelve un DataFrame con las variables relevantes"""
    ruta_al_archivo_nc = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    dataset = nc.Dataset(ruta_al_archivo_nc)
    
    # Extraer variables relevantes
    jd = np.array(dataset.variables['jd'][:])
    tspan = pd.to_datetime(datenum_to_datetime(jd))
    
    Hm = np.array(dataset.variables['Hm'][:]).flatten()
    Hs = np.array(dataset.variables['Hs'][:]).flatten()
    Tp = np.array(dataset.variables['Tp'][:]).flatten()
    Dir = np.array(dataset.variables['Dir'][:]).flatten()
    VarDir = np.array(dataset.variables['VarDir'][:]).flatten()
    DirSpec = np.array(dataset.variables['DirSpec'][:])
    
    # Crear un DataFrame
    data_dict = {
        'tspan': tspan,  # Convertir tiempo a formato datetime
        'Hs': Hs,
        'Hmax': Hm,
        'Tp': Tp,
        'dir': Dir,
        'vardir': VarDir,
    }

    df = pd.DataFrame(data_dict)
    return df, DirSpec


############ METEO ##########
# 1. Cargar memoria .TXT de meteorológicos

# 2. Cargar telemetria .dat de meteorológicos

# 3. Cargar pickle de meteorológicos crudo

# 4. Cargar pickle de meteorológicos validado

# 5. Cargar NETCDF de meteorológicos



################### FUNCIONES AUXILIARES ###################
def crear_indices_para_crudos_dat_o_txt(tipo):
    """"
        Crea un diccionario con los índices de las columnas relevantes para cada tipo de mensaje (viento, oleaje, corrientes) y para cada tipo de archivo (crudo o validado)
    """
    indices = {
        "pos_msg": 5,
        "msg_corrientes": 4,
        "msg_oleaje": 3,
        "msg_meteo": 1,
        
        "temp_adpc": 7,
        "rap_dir": 9, 
        
        "Tp": 7,
        "Hs": 8,
        "Hmax": 9,
        "dir_oleaje": 10,
        "vardir_oleaje": 11,
        
        "presion": 7,
        "humedad": 8,
        "temp_aire": 9,
        "dir_viento_mecanico": 10,
        "rap_viento_mecanico": 11,
        "dir_viento_sonico": 12,
        "rap_viento_sonico": 13
    }
    if tipo == "mem":
        for key in indices.keys():
            indices[key] += 1
    
    return indices



def separar_linea_de_dat_txt_corrientes(linea, indices):
    """" 
    Recibe una línea de un archivo .dat o .txt de corrientes; cada línea representa una medición (un registro).
    Esta función extrae la información relevante de esa línea y devuelve un DataFrame con esa información.
    """
    try:
        msg = int(linea.split(",")[indices["pos_msg"]])
    except:
        return None
    
    if msg != indices["msg_corrientes"]:
        return None
    
    tspan = get_tspan(linea)
    
    # Rap y dir
    rap_dir = linea.split(",")[indices["rap_dir"]]
    
    if rap_dir == '':
        return None
    
    rap = rap_dir.split("@&2C")[0::2] # [nivel]
    dir = rap_dir.split("@&2C")[1::2] # [nivel]
    
    
    # Temp adpc
    temp_adpc = linea.split(",")[indices["temp_adpc"]]
    
    tmp_dict = {}
    for inivel in range(1,len(rap)+1):
        tmp_dict[f"rap_{inivel}"] = []
        tmp_dict[f"dir_{inivel}"] = []
        
        if rap[inivel-1] == "NaN":
            tmp_dict[f"rap_{inivel}"] = np.nan
        else:
            tmp_dict[f"rap_{inivel}"] = np.float32(rap[inivel-1])
        
        if dir[inivel-1] == "NaN":
            tmp_dict[f"dir_{inivel}"] = np.nan
        else:
            tmp_dict[f"dir_{inivel}"] = np.float32(dir[inivel-1])
    
    output_dict = {
        "tspan": tspan,
        "temp_adpc": temp_adpc
    }
    
    for key, values in tmp_dict.items():
        output_dict[key] = values
    
    return output_dict


def leer_datos_de_pickle(ruta_archivo):
    with open(ruta_archivo, 'rb') as file:
        data = pickle.load(file)
    return data


def concatenar_df(df1, nombre_df1, df2, nombre_df2):
    """Concatena dos dataframes por filas; para las mismas fechas que df1"""
    
    if df1.empty:
        return df2
    
    for col_df1 in df1.columns:
        if col_df1 != "tspan":
            df1.rename(columns={col_df1: f"{col_df1}_{nombre_df1}"}, inplace=True)
            
    df_concatenado = pd.merge(df1, df2, left_on="tspan", right_on="tspan", how="inner")
    return df_concatenado


def crear_df_inicial(fecha_de_inicio, fecha_final):
    """ Crea un dataframe con una columna de tiempo (tspan) con el rango de fechas seleccionado; las fechas serán redondeadas a horas exactas; ejemplo 10:02, o 10:50 se redondeará a 10:00"""
    tspan = pd.date_range(start=fecha_de_inicio, end=fecha_final, freq='h')
    df = pd.DataFrame({"tspan": tspan})
    return df


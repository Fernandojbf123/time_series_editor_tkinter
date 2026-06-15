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

def listar_funciones_de_carga():
    lista_de_funciones = [
        "cargar_memoria_adcp_csv",
        "cargar_telemetria_adcp_dat",
        "cargar_pickle_adcp",
        "cargar_nc_adcp",
        "cargar_pickle_oleaje",
        "cargar_nc_oleaje",
        "cargar_pickle_meteo",
        "cargar_nc_meteo"
    ]
    return print(lista_de_funciones)

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
        elif "amp" in column.lower():
            output_df[column] = pd.to_numeric(joined_df[column])
    
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
        
    ae = np.full((cantidad_de_niveles, 4, len(output_df)), np.nan)
    idx = output_df.columns.get_loc('Amp1#1')
    for col in output_df.columns:
        if "Amp".lower() in col.lower():
            name = col.split("#")[0]
            itrans = int(name.lower().replace("amp",""))
            nivel = int(col.split("#")[1])
            ae[nivel-1,itrans-1,:] = np.array(pd.to_numeric(output_df.iloc[:, idx]))
            idx += 1
    
    return output_df, ae


# 2. Cargar telemetria .dat del ADCP  
def cargar_telemetria_adcp_dat(ruta_a_carpeta, nombre_de_archivo, indices,fi,fe):
    """ Carga un archivo .dat de telemetría del ADCP y devuelve un DataFrame con las variables relevantes"""
    dict_corrientes = {}
    ruta_a_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    output_df = crear_df_inicial(fi,fe)
    
    
    with open(ruta_a_archivo, 'r', encoding='utf-8') as archivo:
        # Corrientes
        for linea in archivo:
            tmp_dir = separar_linea_de_dat_txt_corrientes(linea, indices)
            if tmp_dir is not None:
                
                date = tmp_dir["tspan"]
                idx = output_df[output_df["tspan"] == date].index[0]
                for key, value in tmp_dir.items():
                    if key != "tspan" and key not in output_df.columns:
                        output_df.loc[:, key] = np.full(len(output_df["tspan"]), np.nan)
                    
                    if key != "tspan":
                        if pd.isna(output_df.at[idx, key]):
                            output_df.at[idx, key] = value
                        else:
                            print(f"Warning: Duplicate entry for {key} at {date}. Existing value: {output_df.at[idx, key]}, New value: {value}. Keeping existing value.")
   
                # for key, value in tmp_dir.items():
                #     if key not in dict_corrientes:
                #         dict_corrientes[key] = []
                #     dict_corrientes[key].append(value)
                
    # output_df = pd.DataFrame(dict_corrientes)
    output_df.sort_values('tspan', inplace=True)
    # output_df.drop_duplicates(subset='tspan', inplace=True, keep='first')
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
    # dataset.close()
    return df, dataset

def cargar_nc_MCT(ruta_a_carpeta, nombre_de_archivo):
    """ Carga el NETCDF del ADCP y devuelve un DataFrame con las variables relevantes"""
    ruta_nc = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    dataset = nc.Dataset(ruta_nc)
    # Extraer variables relevantes
    jd = np.array(dataset.variables['jd'][:])
    tspan = pd.to_datetime(datenum_to_datetime(jd))
    temp = np.array(dataset.variables['Temp'][:]).flatten()
    cond = np.array(dataset.variables['Cond'][:]).flatten()
    sal = np.array(dataset.variables['Sal'][:]).flatten()
    
      # Crear un DataFrame
    output_dict = {
        'tspan': tspan,  # Convertir tiempo a formato datetime
        'temp': temp,
        'cond': cond,
        'sal': sal

    }
    
    df = pd.DataFrame(output_dict)
    # dataset.close()
    return df, dataset

def cargar_concatenado(ruta_a_carpeta,nombre_de_archivo):
    """ Carga el NETCDF concatenado y devuelve un DataFrame con las variables relevantes"""
    ruta_nc = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    dataset = nc.Dataset(ruta_nc)
    
    jd = np.array(dataset.variables['MT'][:])
    tspan = pd.to_datetime(datenum_to_datetime(jd))
        
    u = np.array(dataset.variables['u'][:])
    v = np.array(dataset.variables['v'][:])
    dir, rap = uv2polar(u, v)
    # temp = np.array(dataset.variables['temperature'][:])
    
    # Crear un DataFrame
    output_dict = {
        'tspan': tspan  # Convertir tiempo a formato datetime
    }
    
    
    for inivel in range(1, u.shape[1]+1):
        output_dict[f"rap_{inivel}"] = []
        output_dict[f"dir_{inivel}"] = []
        output_dict[f"rap_{inivel}"] = rap[:, inivel-1]
        output_dict[f"dir_{inivel}"] = dir[:, inivel-1]

    df = pd.DataFrame(output_dict)
    # dataset.close()
    return df, dataset

############ OLEAJE ##########
# 1. Cargar telemtría .dat de oleaje
def cargar_telemetria_oleaje_dat(ruta_a_carpeta, nombre_de_archivo, indices):
    """ Carga un archivo .dat de telemetría de oleaje y devuelve un DataFrame con las variables relevantes"""
    dict_oleaje = {}
    ruta_a_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    with open(ruta_a_archivo, 'r', encoding='utf-8') as archivo:
        # Oleaje
        for linea in archivo:
            tmp_dir = separar_linea_de_dat_txt_oleaje(linea, indices)
            if tmp_dir is not None:
                for key, value in tmp_dir.items():
                    if key not in dict_oleaje:
                        dict_oleaje[key] = []
                    dict_oleaje[key].append(value)
                
    output_df = pd.DataFrame(dict_oleaje)
    output_df.sort_values('tspan', inplace=True)
    output_df.drop_duplicates(subset='tspan', inplace=True, keep='first')
    output_df.reset_index(drop=True, inplace=True)

    return output_df


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
    # dataset.close()
    return df, dataset, DirSpec


############ METEO ##########
# 1. Cargar memoria .TXT de meteorológicos

# 2. Cargar telemetria .dat de meteorológicos
def cargar_telemetria_meteo_dat(ruta_a_carpeta, nombre_de_archivo, indices,fi,fe):
    """ Carga un archivo .dat de telemetría del ADCP y devuelve un DataFrame con las variables relevantes"""
    dict_meteo = {}
    ruta_a_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    output_df = crear_df_inicial(fi,fe)
    
    
    with open(ruta_a_archivo, 'r', encoding='utf-8') as archivo:
        # Meteorológicos
        for linea in archivo:
            tmp_dir = separar_linea_de_dat_txt_meteo(linea, indices)
            if tmp_dir is not None:
                
                date = tmp_dir["tspan"]
                idx = output_df[output_df["tspan"] == date].index[0]
                for key, value in tmp_dir.items():
                    if key != "tspan" and key not in output_df.columns:
                        output_df.loc[:, key] = np.full(len(output_df["tspan"]), np.nan)
                    
                    if key != "tspan":
                        if pd.isna(output_df.at[idx, key]):
                            output_df.at[idx, key] = value
                        else:
                            print(f"Warning: Duplicate entry for {key} at {date}. Existing value: {output_df.at[idx, key]}, New value: {value}. Keeping existing value.")
   
                
    output_df.sort_values('tspan', inplace=True)
    output_df.reset_index(drop=True, inplace=True)

    return output_df 


# 3. Cargar pickle de meteorológicos crudo / validado
def cargar_pickle_meteo(ruta_a_carpeta, nombre_de_archivo):
     ruta_de_archivo = os.path.join(ruta_a_carpeta, nombre_de_archivo)
     df_pkl = leer_datos_de_pickle(ruta_de_archivo)
     output_df = crear_dataframe_viento_desde_pickle(df_pkl)
     return output_df

# 4. Cargar NETCDF de meteorológicos
def cargar_nc_meteo(ruta_a_carpeta, nombre_de_archivo):
    """ Carga el NETCDF del ADCP y devuelve un DataFrame con las variables relevantes"""
    ruta_nc = os.path.join(ruta_a_carpeta, nombre_de_archivo)
    dataset = nc.Dataset(ruta_nc)
    
    # Extraer variables relevantes
    jd = np.array(dataset.variables['jd'][:])
    tspan = pd.to_datetime(datenum_to_datetime(jd))
    Rap2 = np.array(dataset.variables['Rap2'][:]).flatten()
    Dir2 = np.array(dataset.variables['Dir2'][:]).flatten()
    R5s2 = np.array(dataset.variables['R5s2'][:]).flatten()
    R1s2 = np.array(dataset.variables['R1s2'][:]).flatten()
    Rap1 = np.array(dataset.variables['Rap1'][:]).flatten()
    Dir1 = np.array(dataset.variables['Dir1'][:]).flatten()
    R5s1 = np.array(dataset.variables['R5s1'][:]).flatten()
    R1s1 = np.array(dataset.variables['R1s1'][:]).flatten()
    Ta = np.array(dataset.variables['Ta'][:]).flatten()
    Pa = np.array(dataset.variables['Pa'][:]).flatten()
    HR = np.array(dataset.variables['HR'][:]).flatten()
        
    # Crear un DataFrame
    output_dict = {
        'tspan': tspan,  # Convertir tiempo a formato datetime
        'Pa': Pa,
        'Ta': Ta,
        'HR': HR,
        'Rap1': Rap1,
        'Dir1': Dir1,
        'R5s1': R5s1,
        'R1s1': R1s1,
        'R5s2': R5s2,
        'R1s2': R1s2,
        'Rap2': Rap2,
        'Dir2': Dir2
    }
    
    
    df = pd.DataFrame(output_dict)
    # dataset.close()
    return df, dataset


################### FUNCIONES AUXILIARES ###################
class Crear_indices_para_crudos_dat_o_txt():
    """
    Crea un diccionario con los índices de las columnas relevantes para cada tipo de mensaje 
    (viento, oleaje, corrientes) y para cada tipo de archivo (crudo o validado).
    
    Variables disponibles en el diccionario indices:
    
    Generales:
        - pos_msg: Posición del tipo de mensaje en la línea
        - msg_corrientes: Identificador del mensaje de corrientes (4)
        - msg_oleaje: Identificador del mensaje de oleaje (3)
        - msg_meteo: Identificador del mensaje meteorológico (1)
    
    Corrientes (ADCP):
        - termo_sal: Índice de la columna de temperatura del termosalinómetro
        - temp_adpc: Índice de la columna de temperatura del ADCP
        - rap_dir: Índice de la columna con rapidez y dirección de corrientes
    
    Oleaje:
        - Tp: Índice de la columna de período pico
        - Hs: Índice de la columna de altura significativa
        - Hmax: Índice de la columna de altura máxima
        - dir_oleaje: Índice de la columna de dirección del oleaje
        - vardir_oleaje: Índice de la columna de varianza direccional
    
    Meteorológicos:
        - presion: Índice de la columna de presión atmosférica
        - humedad: Índice de la columna de humedad relativa
        - temp_aire: Índice de la columna de temperatura del aire
        - dir_viento_mecanico: Índice de la columna de dirección del viento mecánico
        - rap_viento_mecanico: Índice de la columna de rapidez del viento mecánico
        - dir_viento_sonico: Índice de la columna de dirección del viento sónico
        - rap_viento_sonico: Índice de la columna de rapidez del viento sónico
    
    Parámetros:
        tipo (str): Tipo de archivo a procesar. Valores posibles:
                    - "mem": Datos de memoria (añade +1 a todos los índices)
                    - Otro valor: Datos de telemetría (usa índices base)
    
    Ejemplo de uso:
        >>> # Para archivos de telemetría
        >>> indices_telemetria = Crear_indices_para_crudos_dat_o_txt("realt")
        >>> indices = indices_telemetria.get_indices()
        >>> print(indices["temp_adpc"])  # Output: 7
        
        >>> # Para archivos de memoria
        >>> indices_memoria = Crear_indices_para_crudos_dat_o_txt("mem")
        >>> indices = indices_memoria.get_indices()
        >>> print(indices["temp_adpc"])  # Output: 8 (incrementado en 1)
        
        >>> # Modificar un índice específico
        >>> indices_telemetria.set_index("temp_adpc", 10)
        >>> print(indices_telemetria.get_indices()["temp_adpc"])  # Output: 10
        
        >>> # Ver todas las claves disponibles
        >>> indices_telemetria.muestra_indices()
    """
    def __init__(self, tipo):
        self.tipo = tipo
        self.indices = {
            "pos_msg": 5,
            "msg_corrientes": 4,
            "msg_oleaje": 3,
            "msg_meteo": 1,
        
            "termo_sal": 6,
            "temp_adpc": 7,
            "rap_dir": 9, 
            
            "Tp": 7,
            "Hs": 8,
            "Hmax": 9,
            "dir_oleaje": 10,
            "vardir_oleaje": 11,
            
            "presion": 7,
            "temp_aire": 8,
            "HR": 9,
            "dir_viento_mecanico": 11,
            "rap_viento_mecanico": 10,
            "dir_viento_sonico": 13,
            "rap_viento_sonico": 12
        }
        if tipo == "mem":
            for key in self.indices.keys():
                self.indices[key] += 1
    
    def muestra_indices(self):
        """
        Imprime todas las claves disponibles en el diccionario de índices.
        
        Ejemplo de uso:
            >>> indices = Crear_indices_para_crudos_dat_o_txt("telemetria")
            >>> indices.muestra_indices()
            dict_keys(['pos_msg', 'msg_corrientes', 'msg_oleaje', 'msg_meteo', ...])
        """
        print(self.indices.keys())
    
    def set_index(self, key, value):
        """
        Modifica el valor de un índice específico en el diccionario.
        
        Parámetros:
            key (str): Nombre de la clave del índice a modificar
            value (int): Nuevo valor para el índice
            
        Raises:
            KeyError: Si la clave no existe en el diccionario de índices
        
        Ejemplo de uso:
            >>> indices = Crear_indices_para_crudos_dat_o_txt("telemetria")
            >>> indices.set_index("temp_adpc", 12)
            >>> print(indices.get_indices()["temp_adpc"])  # Output: 12
            
            >>> # Intento de modificar una clave inexistente
            >>> indices.set_index("clave_invalida", 5)  # Lanza KeyError
        """
        if key in self.indices:
            self.indices[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in indices.")
    
    def get_indices(self):
        """
        Devuelve el diccionario completo de índices.
        
        Returns:
            dict: Diccionario con todos los índices configurados
        
        Ejemplo de uso:
            >>> indices = Crear_indices_para_crudos_dat_o_txt("telemetria")
            >>> todos_los_indices = indices.get_indices()
            >>> print(todos_los_indices["Hs"])  # Output: 8
            >>> print(todos_los_indices["dir_oleaje"])  # Output: 10
        """
        return self.indices


def separar_linea_de_dat_txt_meteo(linea, indices):
    """ Recibe una línea de un archivo .dat o .txt de meteorológicos; cada línea representa una medición (un registro)."""
    try:
        msg = int(linea.split(",")[indices["pos_msg"]])
    except:
        return None
    
    if msg != indices["msg_meteo"]:
        return None
    
    tspan = get_tspan(linea)
    
    # Presión, temperatura del aire y humedad relativa
    presion = np.nan
    if np.array(linea.split(",")[indices["presion"]]) != '':
        presion = np.array(linea.split(",")[indices["presion"]])
        presion = presion.astype(np.float32)
    
    temp_aire = np.nan
    if np.array(linea.split(",")[indices["temp_aire"]]) != '':
        temp_aire = np.array(linea.split(",")[indices["temp_aire"]])
        temp_aire = temp_aire.astype(np.float32)
    
    humedad_relativa = np.nan
    if np.array(linea.split(",")[indices["HR"]]) != '':
        humedad_relativa = np.array(linea.split(",")[indices["HR"]])
        humedad_relativa = humedad_relativa.astype(np.float32)
    
    # Viento mecánico
    dir_viento_mecanico = np.nan
    rap_viento_mecanico = np.nan
    if np.array(linea.split(",")[indices["dir_viento_mecanico"]]) != '' and np.array(linea.split(",")[indices["rap_viento_mecanico"]]) != '':
        dir_viento_mecanico = np.array(linea.split(",")[indices["dir_viento_mecanico"]])
        rap_viento_mecanico = np.array(linea.split(",")[indices["rap_viento_mecanico"]])
        dir_viento_mecanico = dir_viento_mecanico.astype(np.float32)
        rap_viento_mecanico = rap_viento_mecanico.astype(np.float32)
    
    # Viento sónico
    dir_viento_sonico = np.nan
    rap_viento_sonico = np.nan
    if np.array(linea.split(",")[indices["dir_viento_sonico"]]) != '' and np.array(linea.split(",")[indices["rap_viento_sonico"]]) != '':
        dir_viento_sonico = np.array(linea.split(",")[indices["dir_viento_sonico"]])
        rap_viento_sonico = np.array(linea.split(",")[indices["rap_viento_sonico"]])



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
    
    # Temperatura
    temp_adpc = np.nan
    if np.array(linea.split(",")[indices["temp_adpc"]]) != '':
        temp_adcp = np.array(linea.split(",")[indices["temp_adpc"]])
        temp_adpc = temp_adcp.astype(np.float32)
    
    temp_termo = np.nan
    if np.array(linea.split(",")[indices["termo_sal"]]) != '':
        temp_termo = np.array(linea.split(",")[indices["termo_sal"]])
        temp_termo = temp_termo.astype(np.float32)
            
    
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
        "temp_adpc": temp_adpc,
        "temp_termo": temp_termo
    }
    
    for key, values in tmp_dict.items():
        output_dict[key] = values
    
    return output_dict


def separar_linea_de_dat_txt_oleaje(linea, indices):
    """" 
    Recibe una línea de un archivo .dat o .txt de oleaje; cada línea representa una medición (un registro).
    Esta función extrae la información relevante de esa línea y devuelve un DataFrame con esa información.
    """
    try:
        msg = int(linea.split(",")[indices["pos_msg"]])
    except:
        return None
    
    if msg != indices["msg_oleaje"]:
        return None
    
    tspan = get_tspan(linea)
    
    print("PENDIENTE TERMINAR ESTA FUNCION")


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

def comprobar_ae_csv(ae: np.ndarray, fecha_de_inicio: str, fecha_final: str) -> None: 
    esperados = pd.date_range(start=pd.to_datetime(fecha_de_inicio, format='%d/%m/%Y %H:%M'), end=pd.to_datetime(fecha_final, format='%d/%m/%Y %H:%M'), freq='h')
    count_valid = 0
    for iday in range(0, ae.shape[2]):
        if ~np.isnan(ae[:, :, iday]).all():
            count_valid += 1
    
    print(f"Cantidad de días con datos válidos: {count_valid} de {len(esperados)} esperados.")
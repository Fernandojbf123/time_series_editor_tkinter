import os
import pandas as pd

from services.DataFrame_maker import *

def getNombreBoya(ruta_a_archivo):
    ruta_normalizada = os.path.normpath(ruta_a_archivo)
    partes = ruta_normalizada.split(os.path.sep)
    nombre_boya = partes[-3].replace("-", "_")
    return nombre_boya

def selector_de_archivos(ruta, mensaje, tipo):
    """"Devuelve la ruta al archivo crudo y al archivo validado"""
    archivos = os.listdir(ruta)
    ruta_de_archivos = []
    for archivo in archivos:  
        if f"msj{mensaje}" in archivo and f"_crudo_unido_{tipo}_" in archivo and archivo.endswith('.pkl'):
            ruta_de_archivos.append(os.path.normpath(os.path.join(ruta, archivo)))
        if f"msj{mensaje}" in archivo and f"_validados_{tipo}_" in archivo and archivo.endswith('.pkl'):
            ruta_de_archivos.append(os.path.normpath(os.path.join(ruta, archivo)))
        
    return ruta_de_archivos


def cargar_pickle_crudo_y_validado(rutas_de_archivos, msg): 
    dict = {}
    for ruta_de_archivo in rutas_de_archivos:
        df = leer_datos_de_pickle(ruta_de_archivo)
        nombre_boya = getNombreBoya(ruta_de_archivo)
        
        nombre_boya_final = f"{nombre_boya}_validado"
        if "crudo_unido_" in ruta_de_archivo:
            nombre_boya_final = f"{nombre_boya}_crudo" 
        
        if msg == 1: # Viento
            dict[nombre_boya_final] = crear_dataframe_viento_desde_pickle(df)
        elif msg == 3 or msg == 23: # Oleaje    
            dict[nombre_boya_final] = crear_dataframe_oleaje_desde_pickle(df)
        elif msg == 4 or msg == 24: # Corrientes
            dict[nombre_boya_final], prof = crear_dataframe_corrientes_desde_pickle(df)
    
    return dict

def crear_dataframe_de_boyas(dict):
    df = pd.DataFrame()
    for key,value in dict.items():
        df = pd.concat([df, value["tspan"]], axis=0)
    df.drop_duplicates(inplace=True)
    df.sort_values("tspan", inplace=True)

    for boya, df_boya in dict.items():
        for col in df_boya.columns:
            if col != "tspan":
                df_boya[col] = df_boya[col].astype(np.float32)
                df = df.merge(df_boya[["tspan", col]].rename(columns={col: f"{col}_{boya}"}), on="tspan", how="left")

    print(df.columns)
    return df

def combinar_dataframes_con_sufijos(df1: pd.DataFrame, df2: pd.DataFrame, sufijo_df1: str, sufijo_df2: str, how: str = 'outer') -> pd.DataFrame:
    """
    Combina dos dataframes basándose en la columna 'tspan' y agrega sufijos personalizados a las columnas.
    
    Parámetros:
    -----------
    df1 : pd.DataFrame
        Primer dataframe a combinar
    df2 : pd.DataFrame
        Segundo dataframe a combinar
    sufijo_df1 : str
        Sufijo a agregar a las columnas del df1 (ej: '_df1', '_BOT1_01')
    sufijo_df2 : str
        Sufijo a agregar a las columnas del df2 (ej: '_df2', '_BOT1_02')
    how : str, default='outer'
        Tipo de merge: 'inner', 'outer', 'left', 'right'
        - 'outer': mantiene todos los tspan de ambos dataframes
        - 'inner': solo tspan que existen en ambos dataframes
        - 'left': mantiene todos los tspan del df1
        - 'right': mantiene todos los tspan del df2
    
    Retorna:
    --------
    pd.DataFrame
        Dataframe combinado con sufijos en las columnas (excepto 'tspan')
    
    Ejemplo:
    --------
    >>> df_combinado = combinar_dataframes_con_sufijos(df1, df2, '_BOT1_01', '_BOT1_02', how='outer')
    """
    # Validar que ambos dataframes tengan columna 'tspan'
    if 'tspan' not in df1.columns or 'tspan' not in df2.columns:
        raise ValueError("Ambos dataframes deben tener una columna llamada 'tspan'")
    
    # Hacer el merge usando pandas con sufijos automáticos
    df_combinado = pd.merge(
        df1, 
        df2, 
        on='tspan', 
        how=how, 
        suffixes=(sufijo_df1, sufijo_df2)
    )
    
    return df_combinado
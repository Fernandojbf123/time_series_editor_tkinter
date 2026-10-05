import os
import pandas as pd

from services.carga_de_datos import *   

def cargar_telemetria_adcp(nombre_de_boya: str, anios: list, meses: list, tipo: str = "validado"):
    """ 
    Entradas:
    
    - nombre_de_boya = "BMT3-10-T45"    
    Los años y meses deben ser listas de la misma longitud, donde cada elemento de la lista de años corresponde al año del mes en la misma posición en la lista de meses. Por ejemplo, si quieres cargar datos de noviembre y diciembre de 2025, y enero a agosto de 2026, entonces:
    - años = [2025,2025,2026,2026,2026,2026,2026,2026,2026] 
    - meses = [11,12,1,2,3,4,5,6,7,8]
    
    Salida:
    - df_concatenado 
    
    """
    msjs = []
    if tipo == "validado":
        msjs = ["msj4_validados_realt","msj24_validados_realt"]
    elif tipo == "crudo":
        msjs = ["msj4_crudo_unido_realt","msj24_crudo_unido_realt"]
    
    
    meses_str = []
    for mes in meses:
        meses_str.append(mes_a_ruta_carpeta(mes))
        
    reporte = indicar_numero_de_reporte(nombre_de_boya)

    df_concatenado = pd.DataFrame()  # Inicializar un DataFrame vacío para almacenar los datos combinados
    for mes, anio in zip(meses_str, anios):
        ruta_a_carpeta = f"\\\\192.168.15.249\\Med_2025-2026\\Reportes_Edit\\Reporte_{reporte}\\{anio}\\{mes}\\{nombre_de_boya}\\DATOS"
        archivos = os.listdir(ruta_a_carpeta)
        for archivo in archivos:
            if (archivo.startswith(msjs[0]) or archivo.startswith(msjs[1])) and archivo.endswith(".pkl") and not archivo.endswith("_copia.pkl"):
                nombre_de_archivo = archivo
                print(f"{nombre_de_boya} - {nombre_de_archivo}")
                df_actual, _ = cargar_pickle_adcp(ruta_a_carpeta, nombre_de_archivo)
                df_concatenado = pd.concat([df_concatenado, df_actual], ignore_index=True)
    
    return df_concatenado


def cargar_telemetria_oleaje(nombre_de_boya: str, anios: list, meses: list, tipo: str = "validado"):
    """ 
    Entradas:
    
    - nombre_de_boya = "BMT3-10-T45"    
    Los años y meses deben ser listas de la misma longitud, donde cada elemento de la lista de años corresponde al año del mes en la misma posición en la lista de meses. Por ejemplo, si quieres cargar datos de noviembre y diciembre de 2025, y enero a agosto de 2026, entonces:
    - años = [2025,2025,2026,2026,2026,2026,2026,2026,2026] 
    - meses = [11,12,1,2,3,4,5,6,7,8]
    
    Salida:
    - df_concatenado
    
    """
    msjs = []
    if tipo == "validado":
        msjs = ["msj3_validados_realt","msj23_validados_realt"]
    elif tipo == "crudo":
        msjs = ["msj3_crudo_unido_realt","msj23_crudo_unido_realt"]
    
    meses_str = []
    for mes in meses:
        meses_str.append(mes_a_ruta_carpeta(mes))
    
    reporte = indicar_numero_de_reporte(nombre_de_boya)
    
    df_concatenado = pd.DataFrame()  # Inicializar un DataFrame vacío para almacenar los datos combinados
    for mes, anio in zip(meses_str, anios):
        ruta_a_carpeta = f"\\\\192.168.15.249\\Med_2025-2026\\Reportes_Edit\\Reporte_{reporte}\\{anio}\\{mes}\\{nombre_de_boya}\\DATOS"
        archivos = os.listdir(ruta_a_carpeta)
        for archivo in archivos:
            if (archivo.startswith(msjs[0]) or archivo.startswith(msjs[1])) and archivo.endswith(".pkl") and not archivo.endswith("_copia.pkl"):
                df_actual = cargar_pickle_oleaje(ruta_a_carpeta, archivo)
                df_concatenado = pd.concat([df_concatenado, df_actual], ignore_index=True)
                    
    return df_concatenado


def cargar_telemetria_meteo(nombre_de_boya: str, anios: list, meses: list, tipo: str = "validado"):
    """ 
    Entradas:
    
    - nombre_de_boya = "BMT3-10-T45"    
    Los años y meses deben ser listas de la misma longitud, donde cada elemento de la lista de años corresponde al año del mes en la misma posición en la lista de meses. Por ejemplo, si quieres cargar datos de noviembre y diciembre de 2025, y enero a agosto de 2026, entonces:
    - años = [2025,2025,2026,2026,2026,2026,2026,2026,2026] 
    - meses = [11,12,1,2,3,4,5,6,7,8]
    
    Salida:
    - df_concatenado
    
    """

    if tipo == "validado":
        tipo = "msj1_validados_realt"
    elif tipo == "crudo":
        tipo = "msj1_crudo_unido_realt"
        

    meses_str = []
    for mes in meses:
        meses_str.append(mes_a_ruta_carpeta(mes))
    
    reporte = indicar_numero_de_reporte(nombre_de_boya)
    
    df_concatenado = pd.DataFrame()  # Inicializar un DataFrame vacío para almacenar los datos combinados
    for mes, anio in zip(meses_str, anios):
        ruta_a_carpeta = f"\\\\192.168.15.249\\Med_2025-2026\\Reportes_Edit\\Reporte_{reporte}\\{anio}\\{mes}\\{nombre_de_boya}\\DATOS"
        archivos = os.listdir(ruta_a_carpeta)
        for archivo in archivos:
            if archivo.startswith(tipo) and archivo.endswith(".pkl") and not archivo.endswith("_copia.pkl"):
                df_actual = cargar_pickle_meteo(ruta_a_carpeta, archivo)
                df_concatenado = pd.concat([df_concatenado, df_actual], ignore_index=True)
                    
    return df_concatenado
                
                
################### AUXILIARES ########################                
def mes_a_ruta_carpeta(mes: int) -> str:
    """
    Convierte un número de mes (1-12) a su nombre correspondiente en español.

    Args:
        mes (int): Número del mes (1-12).

    Returns:
        str: Nombre del mes en español.
    """
    
    if mes < 1 or mes > 12:
        raise ValueError("El número del mes debe estar entre 1 y 12.")
    if type(mes) is not int:
        raise TypeError("El número del mes debe ser un entero.")
    
    meses = {
        1: "01. Enero",
        2: "02. Febrero",
        3: "03. Marzo",
        4: "04. Abril",
        5: "05. Mayo",
        6: "06. Junio",
        7: "07. Julio",
        8: "08. Agosto",
        9: "09. Septiembre",
        10: "10. Octubre",
        11: "11. Noviembre",
        12: "12. Diciembre"
    }
    return meses.get(mes, "Mes inválido")

def indicar_numero_de_reporte(nombre_de_boya: str) -> str:
    """
    Indica el número de reporte correspondiente a un nombre de boya.

    Args:
        nombre_de_boya (str): Nombre de la boya.

    Returns:
        str: Número de reporte correspondiente.
    """
    
    if not isinstance(nombre_de_boya, str):
        raise TypeError("El nombre de la boya debe ser una cadena de texto.")
    if not nombre_de_boya:
        raise ValueError("El nombre de la boya no puede estar vacío.")
    
    tipo = nombre_de_boya.split("-")[0]
    
    reportes = {
       "BOT1": "1.4",
       "BOT2": "2.4",
       "BMT2": "3.4",
       "BMT3": "4.4"
    }
   
    return reportes.get(tipo, "Tipo de boya desconocido")
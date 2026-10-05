import os
import dotenv
import pandas as pd
from services.revisor_del_netcdf.convertir_coordenadas import convertir_cualquier_coordenada_a_grados_decimales

def lee_base_de_datos_excel(boya):
    dotenv.load_dotenv()
    RUTA_NAS = os.getenv("RUTA_NAS")
    ruta_completa = os.path.join(RUTA_NAS, "Base_de_datos.xlsx")
    df = pd.read_excel(ruta_completa, sheet_name = boya)
    return df

def get_variables_excel(df, ncolumna: int):
    output_excel = {}
    fecha = None
    lat= None
    lon = None
    TiranteDiseno = None
    ProfDiseno_adcp = None
    ProfDiseno_oleaje = None
    ProfDiseno_microcat = None
    AlturaDiseno_ane_mec = None
    AlturaDiseno_ane_son = None
    AlturaDiseno_higrometro = None
    AlturaDiseno_barometro = None
    TiranteEstimado = None
    serial_adcp = None
    serial_oleaje = None
    serial_microcat = None
    serial_datalogger = None
    
    for row in df.itertuples():
        var_name= row[1]
        try:
            if var_name.lower() == "latitud" or var_name.lower() == "lat":
                lat = convertir_cualquier_coordenada_a_grados_decimales(row[ncolumna])
            elif var_name.lower() == "longitud" or var_name.lower() == "lon":
                lon = convertir_cualquier_coordenada_a_grados_decimales(row[ncolumna])
            elif var_name.lower() == "tirante_dis":
                TiranteDiseno = row[ncolumna]
            elif var_name.lower() == "profundidad_adcp":
                ProfDiseno_adcp = row[ncolumna]
            elif var_name.lower() == "profundidad_oleaje":
                ProfDiseno_oleaje = row[ncolumna]
            elif var_name.lower() == "profundidad_microcat":
                ProfDiseno_microcat = row[ncolumna]
            elif var_name.lower() == "altura_ane_mec":
                AlturaDiseno_ane_mec = row[ncolumna]
            elif var_name.lower() == "altura_ane_son":
                AlturaDiseno_ane_son = row[ncolumna]
            elif var_name.lower() == "altura_barometro":
                AlturaDiseno_barometro = row[ncolumna]
            elif var_name.lower() == "altura_higrometro":
                AlturaDiseno_higrometro = row[ncolumna]
            elif var_name.lower() == "tirante_real":
                TiranteEstimado = row[ncolumna]
            elif var_name.lower() == "adcp":
                serial_adcp = row[ncolumna]
            elif var_name.lower() == "oleaje_primario":
                serial_oleaje = row[ncolumna]
            elif var_name.lower() == "microcat":
                serial_microcat = row[ncolumna]
            elif var_name.lower() == "datalogger":
                serial_datalogger = row[ncolumna]
            elif var_name.lower() == "fecha":
                fecha = row[ncolumna]
        except:
            continue
        
    
    output_excel["fecha"] = fecha
    output_excel["Lat"] = lat
    output_excel["Lon"] = lon
    output_excel["TiranteDiseno"] = TiranteDiseno
    output_excel["ProfDiseno_adcp"] = ProfDiseno_adcp
    output_excel["ProfDiseno_oleaje"] = ProfDiseno_oleaje
    output_excel["ProfDiseno_microcat"] = ProfDiseno_microcat
    output_excel["AlturaDiseno_ane_mec"] = AlturaDiseno_ane_mec
    output_excel["AlturaDiseno_ane_son"] = AlturaDiseno_ane_son
    output_excel["AlturaDiseno_barometro"] = AlturaDiseno_barometro
    output_excel["AlturaDiseno_higrometro"] = AlturaDiseno_higrometro
    output_excel["TiranteEstimado"] = TiranteEstimado
    output_excel["serial_adcp"] = serial_adcp
    output_excel["serial_oleaje"] = serial_oleaje
    output_excel["serial_microcat"] = serial_microcat
    output_excel["serial_datalogger"] = serial_datalogger
    
    return output_excel
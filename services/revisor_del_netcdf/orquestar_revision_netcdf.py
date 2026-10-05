import os
from services.revisor_del_netcdf.leer_base_de_datos_excel import lee_base_de_datos_excel, get_variables_excel
from services.revisor_del_netcdf.get_excel_column import get_excel_column
from services.revisor_del_netcdf.test_oleaje import test_oleaje
from services.revisor_del_netcdf.test_corrientes import test_corrientes
from services.revisor_del_netcdf.test_MCT import test_MCT
from services.revisor_del_netcdf.test_meteo import test_meteo
from services.revisor_del_netcdf.variables_netcdf import Oleaje, Corrientes, MCT, Meteo

def orquestar_revision_netcdf(ruta_completa, boya, tipo):
    
    if tipo == "oleaje":
        archivos_netcdf = [f for f in os.listdir(ruta_completa) if f.endswith('.nc') and ("TRIAXYS" in f or "MOTUS" in f)]
    elif tipo == "corrientes":
        archivos_netcdf = [f for f in os.listdir(ruta_completa) if f.endswith('.nc') and ("SIG" in f or "WH" in f)]
    elif tipo == "mct":
        archivos_netcdf = [f for f in os.listdir(ruta_completa) if f.endswith('.nc') and ("MCT" in f)]
    elif tipo == "meteo":
        archivos_netcdf = [f for f in os.listdir(ruta_completa) if f.endswith('.nc') and ("METEO" in f)]
    else: 
        raise ValueError("Tipo de dato a cargar no reconocido")
    
    
    
    for iarchivo in range(len(archivos_netcdf)):
        numero_de_archivo = iarchivo
        ruta_al_archivo_netcdf = os.path.join(ruta_completa, archivos_netcdf[numero_de_archivo])
        nombre_del_archivo_netcdf = archivos_netcdf[numero_de_archivo].split(".nc")[0]
        
        if tipo == "oleaje":
            nc = Oleaje()
        elif tipo == "corrientes":
            nc = Corrientes()
        elif tipo == "mct":
            nc = MCT()
        elif tipo == "meteo":
            nc = Meteo()
        else: 
            raise ValueError("Tipo de dato a cargar no reconocido")
        nc.set_variables(ruta_al_archivo_netcdf)
        df = lee_base_de_datos_excel(boya)
        columna_excel = get_excel_column(df, nombre_del_archivo_netcdf)
        excel_dict = get_variables_excel(df, columna_excel)
        print(f"****{nombre_del_archivo_netcdf}****")
        
        if tipo == "oleaje":
            test_oleaje(nc, excel_dict, nombre_del_archivo_netcdf)
        elif tipo == "corrientes":
            test_corrientes(nc, excel_dict, nombre_del_archivo_netcdf)
        elif tipo == "mct":
            test_MCT(nc, excel_dict, nombre_del_archivo_netcdf)
        elif tipo == "meteo":
            test_meteo(nc, excel_dict, nombre_del_archivo_netcdf)
        else: 
            raise ValueError("Tipo de dato a cargar no reconocido")
        print("\n\n")
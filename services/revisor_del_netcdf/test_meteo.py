import numpy as np
from services.revisor_del_netcdf.test_basico import *

def check_if_in_range(nc_datos) -> None:
    try:
        R1s1 = nc_datos.R1s1
    except: 
        R1s1 = None
    try:
        R5s1 = nc_datos.R5s1
    except:
        R5s1 = None
    try:
        R1s2 = nc_datos.R1s2
    except:
        R1s2 = None
    try:
        R5s2 = nc_datos.R5s2
    except:
        R5s2 = None
    
    if R1s1 is None:
        print("❌ Variable R1s1 no encontrada en el archivo NetCDF.")
    if R5s1 is None:
        print("❌ Variable R5s1 no encontrada en el archivo NetCDF.")
    if R1s2 is None:
        print("❌ Variable R1s2 no encontrada en el archivo NetCDF.")
    if R5s2 is None:
        print("❌ Variable R5s2 no encontrada en el archivo NetCDF.")
    
    
    if R1s1 is not None and R5s1 is not None and np.nanmean(R1s1) > np.nanmean(R5s1):
        print("✅ R1s1 tiene un valor máximo mayor que R5s1")
    else:
        print("❌ R1s1 es menor queR5s1: Las rachas del anemómetro primario están invertidas")
        
    if R1s2 is not None and R5s2 is not None and np.nanmean(R1s2) > np.nanmean(R5s2):
        print("✅ R1s2 tiene un valor máximo mayor que R5s2")
    else:
        print("❌ R1s2 es menor que R5s2: Las rachas del anemómetro secundario están invertidas")
    
    if R1s1 is not None and R1s2 is not None and np.nanmean(R1s1) > np.nanmean(R1s2):
        print("✅ R1s1 tiene un valor máximo mayor que R1s2")
    else:
        print("❌ R1s1 es MENOR que R1s2: Se colocó el anemómetro mecánico como primario")
    
    
def check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos_esperada, nombre_de_la_variable, variables_faltantes):
    if cantidad_de_datos_de_la_variable == cantidad_de_datos_esperada:
        print(f"✅ Variable {nombre_de_la_variable} tiene la misma cantidad de datos que la variable jd")
        variables_faltantes.remove(nombre_de_la_variable)
    else:
        print(f"❌ Variable {nombre_de_la_variable} NO tiene la misma cantidad de datos que la variable jd")
        print(f"{cantidad_de_datos_de_la_variable} --- Cantidad de datos de la variable {nombre_de_la_variable} del netCDF")
        print(f"{cantidad_de_datos_esperada} --- Cantidad de datos de la variable jd del netCDF")


def test_prof_diseno_meteo(datos_nc, excel: dict):
    if datos_nc.AlturaDiseno_ane_mec == excel["AlturaDiseno_ane_mec"]:
        print("✅ Altura de diseño del anemómetro mecánico coincide con la base de datos")
    else:
        print("❌ Altura de diseño del anemómetro mecánico NO coincide con la base de datos")
        print(f"{datos_nc.AlturaDiseno_ane_mec} --- Altura de diseño del anemómetro mecánico del netCDF")
        print(f"{excel['AlturaDiseno_ane_mec']} --- Altura de diseño del anemómetro mecánico de la base de datos")
    if datos_nc.AlturaDiseno_ane_son == excel["AlturaDiseno_ane_son"]:
        print("✅ Altura de diseño del anemómetro sónico coincide con la base de datos")
    else:
        print("❌ Altura de diseño del anemómetro sónico NO coincide con la base de datos")
        print(f"{datos_nc.AlturaDiseno_ane_son} --- Altura de diseño del anemómetro sónico del netCDF")
        print(f"{excel['AlturaDiseno_ane_son']} --- Altura de diseño del anemómetro sónico de la base de datos")
    if datos_nc.AlturaDiseno_higrometro == excel["AlturaDiseno_higrometro"]:
        print("✅ Altura de diseño del higrómetro coincide con la base de datos")
    else:
        print("❌ Altura de diseño del higrómetro NO coincide con la base de datos")
        print(f"{datos_nc.AlturaDiseno_higrometro} --- Altura de diseño del higrómetro del netCDF")
        print(f"{excel['AlturaDiseno_higrometro']} --- Altura de diseño del higrómetro de la base de datos")
    if datos_nc.AlturaDiseno_barometro == excel["AlturaDiseno_barometro"]:
        print("✅ Altura de diseño del barómetro coincide con la base de datos")
    else:
        print("❌ Altura de diseño del barómetro NO coincide con la base de datos")
        print(f"{datos_nc.AlturaDiseno_barometro} --- Altura de diseño del barómetro del netCDF")
        print(f"{excel['AlturaDiseno_barometro']} --- Altura de diseño del barómetro de la base de datos")
        
        
def test_variables_meteo(datos_nc):
    variables = ["Rap1","Dir1","R1s1","R5s1","Rap2","Dir2","R1s2","R5s2","Pa","Ta","HR"]
    variables_faltantes = variables.copy()
    cantidad_de_datos = len(datos_nc.jd)
    
    for variable in variables:
        var_values = getattr(datos_nc, variable)
        cantidad_de_datos_de_la_variable = len(var_values)
        check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)

    check_if_in_range(datos_nc)     
                     
    if len(variables_faltantes) > 0:
        print(f"❌ ❌ ❌Las siguientes variables no se encontraron en el archivo NetCDF: {', '.join(variables_faltantes)}")
        
        
def test_meteo(datos_nc, excel: dict, nombre_del_archivo_netcdf: str):
    print("---- Test básico ----")
    test_basico(datos_nc, excel, nombre_del_archivo_netcdf)
    print("\n---- Test profundidad de diseño meteo ----")
    test_prof_diseno_meteo(datos_nc, excel)
    print("\n---- Test variables de meteo ----")
    test_variables_meteo(datos_nc)

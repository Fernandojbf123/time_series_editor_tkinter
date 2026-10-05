import numpy as np
from services.revisor_del_netcdf.test_basico import *

def check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos_esperada, nombre_de_la_variable, variables_faltantes):
    if cantidad_de_datos_de_la_variable == cantidad_de_datos_esperada:
        print(f"✅ Variable {nombre_de_la_variable} tiene la misma cantidad de datos que la variable jd")
        variables_faltantes.remove(nombre_de_la_variable)
    else:
        print(f"❌ Variable {nombre_de_la_variable} NO tiene la misma cantidad de datos que la variable jd")
        print(f"{cantidad_de_datos_de_la_variable} --- Cantidad de datos de la variable {nombre_de_la_variable} del netCDF")
        print(f"{cantidad_de_datos_esperada} --- Cantidad de datos de la variable jd del netCDF")


def test_prof_diseno_mct(datos_nc, excel: dict):
    if datos_nc.ProfDiseno == np.float32(excel["ProfDiseno_microcat"]):
        print("✅ Profundidad de diseño coincide con la base de datos")
    else:
        print("❌ Profundidad de diseño NO coincide con la base de datos")
        print(f"{datos_nc.ProfDiseno} --- Profundidad de diseño del netCDF")
        print(f"{excel['ProfDiseno_microcat']} --- Profundidad de diseño de la base de datos")
        
        
def test_variables_mct(datos_nc):
    variables = ["Temp", "Cond", "Sal"]
    variables_faltantes = variables.copy()
    cantidad_de_datos = len(datos_nc.jd)
    
    for variable in variables:
        var_values = getattr(datos_nc, variable)
        if len(var_values) == cantidad_de_datos:
            print(f"✅ Variable {variable} tiene la misma cantidad de datos que la variable jd")
            variables_faltantes.remove(variable)
        else:
            print(f"❌ Variable {variable} NO tiene la misma cantidad de datos que la variable jd")
    if len(variables_faltantes) > 0:
        print(f"❌ ❌ ❌Las siguientes variables no se encontraron en el archivo NetCDF: {', '.join(variables_faltantes)}")
        
        
def test_MCT(datos_nc, excel: dict, nombre_del_archivo_netcdf: str):
    print("---- Test básico ----")
    test_basico(datos_nc, excel, nombre_del_archivo_netcdf)
    print("\n---- Test profundidad de diseño MCT ----")
    test_prof_diseno_mct(datos_nc, excel)
    print("\n---- Test variables de MCT ----")
    test_variables_mct(datos_nc)
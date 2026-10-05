import numpy as np
from services.revisor_del_netcdf.test_basico import *

def check_if_in_range(var_values: list, variable_name: str) -> None:
    if variable_name.lower() == "Heading".lower():
        if 0 <= np.nanmin(var_values) < 180 and 180 < np.nanmax(var_values) <= 360:
            print(f"✅ Variable {variable_name} tiene un valor dentro del rango esperado (0-360 grados)")
        else:
            print(f"❌ Variable {variable_name} tiene un valor fuera del rango esperado (0-360 grados)")
    
    if variable_name.lower() == "Roll".lower():
        if -185 <= np.nanmin(var_values) <= -175 or 175 <= np.nanmax(var_values) <= 185:
            print(f"✅ Variable {variable_name} tiene un valor dentro del rango esperado (+- 180 grados)")
        else:
            print(f"❌ Variable {variable_name} tiene un valor fuera del rango esperado (+- 180 grados)")
            
    if variable_name.lower() == "Pitch".lower():
        if -10 <= np.nanmin(var_values) <= -2 or 2 <= np.nanmax(var_values) <= 15:
            print(f"✅ Variable {variable_name} tiene un valor dentro del rango esperado (+- 10 grados)")
        else:
            print(f"❌ Variable {variable_name} tiene un valor fuera del rango esperado (+- 10 grados)")

def check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos_esperada, nombre_de_la_variable, variables_faltantes):
    if cantidad_de_datos_de_la_variable == cantidad_de_datos_esperada:
        print(f"✅ Variable {nombre_de_la_variable} tiene la misma cantidad de datos que la variable jd")
        variables_faltantes.remove(nombre_de_la_variable)
    else:
        print(f"❌ Variable {nombre_de_la_variable} NO tiene la misma cantidad de datos que la variable jd")
        print(f"{cantidad_de_datos_de_la_variable} --- Cantidad de datos de la variable {nombre_de_la_variable} del netCDF")
        print(f"{cantidad_de_datos_esperada} --- Cantidad de datos de la variable jd del netCDF")


def check_cantidad_de_niveles(cantidad_de_niveles_de_la_variable, cantidad_de_niveles_esperada, nombre_de_la_variable):
    if cantidad_de_niveles_de_la_variable == cantidad_de_niveles_esperada:
        print(f"✅ Variable {nombre_de_la_variable} tiene la misma cantidad de niveles reportados en la variable depth")
    else:
        print(f"❌ Variable {nombre_de_la_variable} NO tiene la misma cantidad de niveles reportados en la variable depth")
        print(f"{cantidad_de_niveles_de_la_variable} --- Cantidad de niveles de la variable {nombre_de_la_variable} del netCDF")
        print(f"{cantidad_de_niveles_esperada} --- Cantidad de niveles de la variable depth del netCDF")


def test_prof_diseno_adcp(datos_nc, excel: dict):
    if datos_nc.ProfDiseno == np.float32(excel["ProfDiseno_adcp"]):
        print("✅ Profundidad de diseño coincide con la base de datos")
    else:
        print("❌ Profundidad de diseño NO coincide con la base de datos")
        print(f"{datos_nc.ProfDiseno} --- Profundidad de diseño del netCDF")
        print(f"{excel['ProfDiseno_adcp']} --- Profundidad de diseño de la base de datos")
        
        
def test_variables_corrientes(datos_nc):
    variables = ["u", "v", "ae", "Heading", "Pitch", "Roll", "depth", "Temp"]
    variables_faltantes = variables.copy()
    cantidad_de_datos = len(datos_nc.jd)
    
    for variable in variables:
        var_values = getattr(datos_nc, variable)
        
        if variable.lower() == "Heading".lower():
            cantidad_de_datos_de_la_variable = len(getattr(datos_nc, variable))
            check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)
            check_if_in_range(var_values, variable)
            
        if variable.lower() == "Pitch".lower():
            cantidad_de_datos_de_la_variable = len(getattr(datos_nc, variable))
            check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)
            check_if_in_range(var_values, variable)
            
        if variable.lower() == "Roll".lower():
            cantidad_de_datos_de_la_variable = len(getattr(datos_nc, variable))
            check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)
            check_if_in_range(var_values, variable)
            
        if variable.lower() == "Temp".lower():
            cantidad_de_datos_de_la_variable = len(getattr(datos_nc, variable))
            check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)
            
        if variable.lower() == "u".lower() or variable.lower() == "v".lower():
            cantidad_de_datos_de_la_variable = getattr(datos_nc, variable).shape[0]
            check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)
            
            cantidad_de_niveles = getattr(datos_nc, variable).shape[1]    
            check_cantidad_de_niveles(cantidad_de_niveles, datos_nc.depth.shape[0], variable)
            
                
        if variable.lower() == "ae".lower():
            cantidad_de_datos_de_la_variable = getattr(datos_nc, variable).shape[2]
            check_numero_de_datos(cantidad_de_datos_de_la_variable, cantidad_de_datos, variable, variables_faltantes)
            cantidad_de_niveles = getattr(datos_nc, variable).shape[0]    
            check_cantidad_de_niveles(cantidad_de_niveles, datos_nc.depth.shape[0], variable)

                
        if variable.lower() == "depth".lower():
            print(f"✅ Se encuentra la variable {variable}")
            variables_faltantes.remove(variable)
    
    if len(variables_faltantes) > 0:
        print(f"❌ ❌ ❌Las siguientes variables no se encontraron en el archivo NetCDF: {', '.join(variables_faltantes)}")
        
        
def test_corrientes(datos_nc, excel: dict, nombre_del_archivo_netcdf: str):
    print("---- Test básico ----")
    test_basico(datos_nc, excel, nombre_del_archivo_netcdf)
    print("\n---- Test profundidad de diseño corrientes ----")
    test_prof_diseno_adcp(datos_nc, excel)
    print("\n---- Test variables de corrientes ----")
    test_variables_corrientes(datos_nc)
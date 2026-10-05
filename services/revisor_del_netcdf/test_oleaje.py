import numpy as np
from services.revisor_del_netcdf.test_basico import *
        

def test_prof_diseno_oleaje(datos_nc, excel: dict):
    if datos_nc.ProfDiseno == np.float32(excel["ProfDiseno_oleaje"]):
        print("✅ Profundidad de diseño coincide con la base de datos")
    else:
        print("❌ Profundidad de diseño NO coincide con la base de datos")
        print(f"{datos_nc.ProfDiseno} --- Profundidad de diseño del netCDF")
        print(f"{excel['ProfDiseno_oleaje']} --- Profundidad de diseño de la base de datos")
        
        
def test_variables_oleaje(datos_nc):
    variables = ["Hs", "Hm", "Dir", "Tp", "VarDir", "DirSpec", "grados", "frec"]
    variables_faltantes = variables.copy()
    cantidad_de_datos = len(datos_nc.jd)
    
    for variable in variables:
        if variable != "DirSpec" and variable != "grados" and variable != "frec":
            if len(getattr(datos_nc, variable)) == cantidad_de_datos:
                print(f"✅ Variable {variable} tiene la misma cantidad de datos que la variable jd")
                variables_faltantes.remove(variable)
            else:
                print(f"❌ Variable {variable} NO tiene la misma cantidad de datos que la variable jd")
        
        if variable == "DirSpec":
            if datos_nc.DirSpec.shape[0] == cantidad_de_datos:
                print(f"✅ Variable {variable} tiene la misma cantidad de datos que la variable jd")
                variables_faltantes.remove(variable)
            else:
                print(f"❌ Variable {variable} NO tiene la misma cantidad de datos que la variable jd")

        if variable == "grados":
            if isinstance(datos_nc.grados, np.ndarray) and datos_nc.grados.shape[0] == datos_nc.DirSpec.shape[1]:
                print(f"✅ Variable {variable} tiene la misma cantidad de datos que la segunda dimensión de la variable DirSpec")
                variables_faltantes.remove(variable)
            else:
                print(f"❌ Variable {variable} NO tiene la misma cantidad de datos que la segunda dimensión de la variable DirSpec")
        
        if variable == "frec":
            if isinstance(datos_nc.frec, np.ndarray) and datos_nc.frec.shape[0] == datos_nc.DirSpec.shape[2]:
                print(f"✅ Variable {variable} tiene la misma cantidad de datos que la tercera dimensión de la variable DirSpec")
                variables_faltantes.remove(variable)
            else:
                print(f"❌ Variable {variable} NO tiene la misma cantidad de datos que la tercera dimensión de la variable DirSpec")    
                
    if len(variables_faltantes) > 0:
        print(f"❌ ❌ ❌Las siguientes variables no se encontraron en el archivo NetCDF: {', '.join(variables_faltantes)}")
                
def test_oleaje(datos_nc, excel: dict, nombre_del_archivo_netcdf: str):
    print("---- Test básico ----")
    test_basico(datos_nc, excel, nombre_del_archivo_netcdf)
    print("\n---- Test profundidad de diseño oleaje ----")
    test_prof_diseno_oleaje(datos_nc, excel)
    print("\n---- Test variables de oleaje ----")
    test_variables_oleaje(datos_nc)
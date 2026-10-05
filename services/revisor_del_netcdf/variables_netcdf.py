
import netCDF4
import numpy as np
from services.revisor_del_netcdf.date_functions import datenum_to_datetime

class VariablesNetCDF():
    def __init__(self):
        self.nam = None
        self.Lat = None
        self.Lon = None
        self.TiranteEstimado = None
        self.TiranteDiseno = None
        self.ProfDiseno = None
        self.jd = None
        
    def set_variables(self, ruta_al_netCDF: str):
        variables_faltantes = ["nam", "Lat", "Lon", "TiranteEstimado", "TiranteDiseno", "ProfDiseno", "jd"]
        variables = variables_faltantes.copy()
        with netCDF4.Dataset(ruta_al_netCDF, 'r') as nc:
            for variable in variables:
                if variable == "nam":
                    self.nam = "".join(np.array(nc.variables['nam'][:].flatten()).astype(str))
                    variables_faltantes.remove("nam")
                
                elif variable == "jd":
                    setattr(self, variable, datenum_to_datetime(nc.variables["jd"][:]))    
                    variables_faltantes.remove("jd")
                
                elif variable in variables:
                    setattr(self, variable, np.array(nc.variables[variable][:])[0])
                    variables_faltantes.remove(variable)
                
        
        if len(variables_faltantes) > 0:
            print(f"Las siguientes variables no se encontraron en el archivo NetCDF {ruta_al_netCDF}: {', '.join(variables_faltantes)}")


#### HIJOS DE VARIABLESNetCDF ####
class Corrientes(VariablesNetCDF):
    def __init__(self):
        super().__init__()
        self.u = None
        self.v = None
        self.ae = None
        self.Heading = None
        self.Pitch = None
        self.Roll = None
        self.depth = None
        self.Temp = None
        
    def set_variables(self, ruta_al_netCDF: str):
        super().set_variables(ruta_al_netCDF)
        variables_faltantes = ["u", "v", "ae", "Heading", "Pitch", "Roll", "depth", "Temp"]
        variables = variables_faltantes.copy()
        with netCDF4.Dataset(ruta_al_netCDF, 'r') as nc:
             for variable in variables:
                if variable in list(nc.variables.keys()):
                    setattr(self, variable, np.array(nc.variables[variable][:]))
                    variables_faltantes.remove(variable)
            
        if len(variables_faltantes) > 0:
            print(f"Las siguientes variables no se encontraron en el archivo NetCDF {ruta_al_netCDF}: {', '.join(variables_faltantes)}")
        
class Oleaje(VariablesNetCDF):
    def __init__(self):
        super().__init__()
        self.Hs = None
        self.Hm = None
        self.Dir = None
        self.Tp = None
        self.VarDir = None
        self.DirSpec = None
        self.grados = None
        self.frec = None
        
    def set_variables(self, ruta_al_netCDF: str):
        super().set_variables(ruta_al_netCDF)
        variables_faltantes = ["Hs", "Hm", "Dir", "Tp", "VarDir", "DirSpec", "grados", "frec"]
        variables = variables_faltantes.copy()
        with netCDF4.Dataset(ruta_al_netCDF, 'r') as nc:
            for variable in variables:
                if variable in list(nc.variables.keys()):
                    setattr(self, variable, np.array(nc.variables[variable][:]))
                    variables_faltantes.remove(variable)

        if len(variables_faltantes) > 0:
            print(f"Las siguientes variables no se encontraron en el archivo NetCDF {ruta_al_netCDF}: {', '.join(variables_faltantes)}")


class MCT(VariablesNetCDF):
    def __init__(self):
        super().__init__()
        self.Temp = None
        self.Cond = None
        self.Sal = None
        
    def set_variables(self, ruta_al_netCDF: str):
        super().set_variables(ruta_al_netCDF)
        variables_faltantes = ["Temp", "Cond", "Sal"]
        variables = variables_faltantes.copy()
        with netCDF4.Dataset(ruta_al_netCDF, 'r') as nc:
            for variable in variables:
                if variable in list(nc.variables.keys()):
                    setattr(self, variable, np.array(nc.variables[variable][:]))
                    variables_faltantes.remove(variable)

        if len(variables_faltantes) > 0:
            print(f"Las siguientes variables no se encontraron en el archivo NetCDF {ruta_al_netCDF}: {', '.join(variables_faltantes)}")

class Meteo(VariablesNetCDF):
    def __init__(self):
        super().__init__()
        self.Rap1 = None
        self.Dir1 = None
        self.R1s1 = None
        self.R5s1 = None
        self.Rap2 = None
        self.Dir2 = None
        self.R1s2 = None
        self.R5s2 = None
        self.Pa = None
        self.Ta = None
        self.HR = None
        self.AlturaDiseno_ane_mec = None
        self.AlturaDiseno_ane_son = None
        self.AlturaDiseno_higrometro = None
        self.AlturaDiseno_barometro = None
       
        
    def set_variables(self, ruta_al_netCDF: str):
        super().set_variables(ruta_al_netCDF)
        variables_faltantes = ["ProfDiseno", "Rap1","Dir1","R1s1","R5s1","Rap2","Dir2","R1s2","R5s2","Pa","Ta","HR"]
        variables = variables_faltantes.copy()
        with netCDF4.Dataset(ruta_al_netCDF, 'r') as nc:
            for variable in variables:
                if variable in list(nc.variables.keys()):
                    if variable == "ProfDiseno":
                        alturas = np.array(nc.variables[variable][:])
                        try:
                            self.AlturaDiseno_ane_mec = np.float32(alturas[0].split(":")[-1].strip())
                            self.AlturaDiseno_ane_son = np.float32(alturas[1].split(":")[-1].strip())
                            self.AlturaDiseno_higrometro = np.float32(alturas[2].split(":")[-1].strip())
                            self.AlturaDiseno_barometro = np.float32(alturas[3].split(":")[-1].strip())
                        except:
                            print(f"❌ La variable 'ProfDiseno' debe contener un array con 4 alturas, actualmente tiene esta forma {alturas}")
                    else:
                        setattr(self, variable, np.array(nc.variables[variable][:]))
                    variables_faltantes.remove(variable)
                    
                else:
                    print(f"Variable '{variable}' no encontrada en el archivo NetCDF {ruta_al_netCDF}.")

        if len(variables_faltantes) > 0:
            print(f"Las siguientes variables no se encontraron en el archivo NetCDF {ruta_al_netCDF}: {', '.join(variables_faltantes)}")
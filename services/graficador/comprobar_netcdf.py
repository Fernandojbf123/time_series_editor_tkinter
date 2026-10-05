import os
import pandas as pd
import numpy as np
from services.compartidos.polar2uv import polar2uv

def comprobar_nombre_nc(nombre_de_archivo, nc_data):
    
    nam = "".join(np.array(nc_data["nam"]).flatten().astype(str))
    if nam != nombre_de_archivo.replace(".nc", ""):
        print (f"NAM incorrecto")
    else:
        print(f"NAM correcto")
        
def comprobar_porcentaje_de_variable(nc_data, carpeta_al_excel, nombre_archivo_porcentajes, variables="oleaje"):
    # df_excel = pd.read_excel(os.path.join(carpeta_al_excel, nombre_archivo_porcentajes))
    output_df = pd.DataFrame()
    
    def get_excel_idx_var_name(df_excel):
        output_dict = {}
        var_names = df_excel.iloc[:,0].values
        for var_name in var_names:
            output_dict[var_name] = df_excel[df_excel.iloc[:,0] == var_name].index[0]
        return output_dict
    
    if variables == "oleaje":
        nc_vars = ["Hs", "Hm", "Tp", "dir", "vardir", "dirspec"]
        Hs = np.array(nc_data.variables["Hs"][:]).astype(np.float32).flatten()
        Hm = np.array(nc_data.variables["Hm"][:]).astype(np.float32).flatten()
        Tp = np.array(nc_data.variables["Tp"][:]).astype(np.float32).flatten()
        dir = np.array(nc_data.variables["Dir"][:]).astype(np.float32).flatten()
        vardir = np.array(nc_data.variables["VarDir"][:]).astype(np.float32).flatten()
        dirspec = np.array(nc_data.variables["DirSpec"][:]).astype(np.float32)
        
        ndatos_esperados = Hs.shape[0]
        
        output_df = pd.DataFrame()
        output_df["Variable"] = nc_vars
        output_df["esperados"] = [ndatos_esperados] * len(nc_vars)
        output_df["validados"] = [(~np.isnan(var)).sum() for var in [Hs, Hm, Tp, dir, vardir]] +  [np.nan] 
        count_valid = 0
        for iday in range(0, dirspec.shape[0]):
            if ~np.isnan(dirspec[iday, :, :]).all():
                count_valid += 1
        
        output_df.iloc[-1,2] = count_valid
        output_df["porcentaje_validados"] = output_df["validados"] / output_df["esperados"] * 100
                
    elif variables == "corrientes":
        nc_vars = ["Temp", "u", "v", "ae"]
        u = np.array(nc_data.variables["u"][:]).astype(np.float32)
        v = np.array(nc_data.variables["v"][:]).astype(np.float32)
        temp = np.array(nc_data.variables["Temp"][:]).astype(np.float32).flatten()
        dir, rap = polar2uv(u,v)
        ae = np.array(nc_data.variables["ae"][:]).astype(np.float64)
        ndatos_esperados = rap.shape[0]
        
        output_df = pd.DataFrame()
        
        count_valid = 0
        for iday in range(0, ae.shape[2]):
            if ~np.isnan(ae[:, :, iday]).all():
                count_valid += 1
        
        output_df.loc[0,"Variable"] = "AE"
        output_df.loc[0,"esperados"] = ndatos_esperados
        output_df.loc[0,"validados"] = count_valid
        
        output_df.loc[1,"Variable"] = "Temp adcp"
        output_df.loc[1,"esperados"] = ndatos_esperados
        output_df.loc[1,"validados"] = (~np.isnan(temp)).sum()
        
        ndatos_recibidos = []
        porcentaje_validados = []
        var_name = []
        for inivel in range(0, rap.shape[1]):
            recibido = (~np.isnan(rap[:, inivel])).sum()
            ndatos_recibidos.append(recibido)
            porcentaje_validados.append(recibido / ndatos_esperados * 100)
            var_name.append(f"rap_{inivel+1}")

        df_temporal = pd.DataFrame({
            "Variable": var_name, 
            "esperados": ndatos_esperados, 
            "validados": ndatos_recibidos})
        
        output_df = pd.concat([output_df, df_temporal], axis=0)
        output_df["porcentaje_validados"] = output_df["validados"] / output_df["esperados"] * 100
        
    elif "meteo" in variables:
        nc_vars = ["Pa", "Ta", "HR", "Rap1", "Dir1", "R1s1", "R5s1", "Rap2", "Dir2", "R1s2", "R5s2"]
        Rap2 = np.array(nc_data.variables['Rap2'][:]).flatten()
        Dir2 = np.array(nc_data.variables['Dir2'][:]).flatten()
        R5s2 = np.array(nc_data.variables['R5s2'][:]).flatten()
        R1s2 = np.array(nc_data.variables['R1s2'][:]).flatten()
        Rap1 = np.array(nc_data.variables['Rap1'][:]).flatten()
        Dir1 = np.array(nc_data.variables['Dir1'][:]).flatten()
        R5s1 = np.array(nc_data.variables['R5s1'][:]).flatten()
        R1s1 = np.array(nc_data.variables['R1s1'][:]).flatten()
        Ta = np.array(nc_data.variables['Ta'][:]).flatten()
        Pa = np.array(nc_data.variables['Pa'][:]).flatten()
        HR = np.array(nc_data.variables['HR'][:]).flatten()
        
        ndatos_esperados = Ta.shape[0]
        
        output_df = pd.DataFrame()
        output_df["Variable"] = nc_vars
        output_df["esperados"] = [ndatos_esperados] * len(nc_vars)
        output_df["validados"] = [(~np.isnan(var)).sum() for var in [Pa, Ta, HR, Rap1, Dir1, R1s1, R5s1, Rap2, Dir2, R1s2, R5s2]]
        output_df["porcentaje_validados"] = output_df["validados"] / output_df["esperados"] * 100
    
    return output_df
        
            
        
             
        
             
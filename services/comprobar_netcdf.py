import os
import pandas as pd
import numpy as np
from services.polar2uv import polar2uv

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
            sum = np.nansum(dirspec[iday,:,:])
            if sum > 0:
                count_valid += 1
        
        output_df.iloc[-1,2] = count_valid
        output_df["porcentaje_validados"] = output_df["validados"] / output_df["esperados"] * 100
        
        return output_df
        
    elif variables == "corrientes":
        nc_vars = ["Temp", "u", "v"]
        u = np.array(nc_data.variables["u"][:]).astype(np.float32)
        v = np.array(nc_data.variables["v"][:]).astype(np.float32)
        temp = np.array(nc_data.variables["Temp"][:]).astype(np.float32).flatten()
        dir, rap = polar2uv(u,v)
        
        ndatos_esperados = rap.shape[0]
        
        output_df = pd.DataFrame()
        output_df.loc[0,"Variable"] = "Temp adcp"
        output_df.loc[0,"esperados"] = ndatos_esperados
        output_df.loc[0,"validados"] = (~np.isnan(temp)).sum()
        
        
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
    
    return output_df
        
            
        
             
        
             
import numpy as np

def test_basico(datos_nc, excel: dict, nombre_del_archivo_netcdf: str):
    
    if datos_nc.nam == nombre_del_archivo_netcdf:
        print("✅ Nombre del archivo netCDF coincide con la variable nam del netCDF")
    else:
        print("❌ Nombre del archivo netCDF NO coincide con la variable nam del netCDF")
        print(f"{datos_nc.nam} --- nam")
        print(f"{nombre_del_archivo_netcdf} --- nombre del archivo netCDF")
        
    if round(datos_nc.Lat,2) == np.float32(round(excel["Lat"],2)):
        print("✅ Latitud de instalacion de la base de datos coincide con la del netCDF")
    else:
        print("❌ Latitud de instalacion de la base de datos NO coincide con la del netCDF")
        print(f"{datos_nc.Lat} --- Lat del netCDF")
        print(f"{excel['Lat']} --- Lat de la base de datos")
        
    if round(datos_nc.Lon,2) == np.float32(round(excel["Lon"],2)):
        print("✅ Longitud de instalacion de la base de datos coincide con la del netCDF")
    else:
        print("❌ Longitud de instalacion de la base de datos NO coincide con la del netCDF")
        print(f"{datos_nc.Lon} --- Lon del netCDF")
        print(f"{excel['Lon']} --- Lon de la base de datos")
        
    if datos_nc.TiranteDiseno == excel["TiranteDiseno"]:
        print("✅ Tirante de diseño coincide con la base de datos")
    else:
        print("❌ Tirante de diseño NO coincide con la base de datos")
        print(f"{datos_nc.TiranteDiseno} --- Tirante de diseño del netCDF")
        print(f"{excel['TiranteDiseno']} --- Tirante de diseño de la base de datos")
        
    if datos_nc.TiranteEstimado == excel["TiranteEstimado"]:
        print("✅ Tirante estimado coincide con la base de datos")
    else:
        print("❌ Tirante estimado NO coincide con la base de datos")
        print(f"{datos_nc.TiranteEstimado} --- Tirante estimado del netCDF")
        print(f"{excel['TiranteEstimado']} --- Tirante estimado de la base de datos")
    

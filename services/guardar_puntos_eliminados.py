import os
import matplotlib.dates as mdates
import pandas as pd
from pickle import dump

def guardar_puntos_eliminados(app, ruta_a_carpeta, nombre_de_archivo):
    dict_out = {}
    for key in app.deletion_log.keys():
        idxs = app.deletion_log[key]["idxs"]
        tspan_num = mdates.num2date(app.data.loc[idxs,"tspan"])
        tspan_pd = pd.to_datetime(tspan_num)

        if len(idxs) > 0:
            new_key_name = "".join(key.split("_")[0:2])
            dict_out[new_key_name] = {
                "index": idxs,
                "tspan_num": tspan_num
                }
            
    ruta_completa = os.path.join(ruta_a_carpeta, f"{nombre_de_archivo}.pkl")
    dump(dict_out, open(ruta_completa, "wb"))
    print(f"Archivo guardado en: {ruta_completa}")
    return dict_out
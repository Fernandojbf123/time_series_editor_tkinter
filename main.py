from DataFrame_maker import crear_dataframe_corrientes_desde_pickle, create_sample_data, leer_datos_de_corrientes_pickle
from prueba import InteractivePlotterTk
import os
# from GraCorrector import GraCorrector

from Gra import GraficoInteractivo
# %matplotlib qt
import pandas as pd
import numpy as np


carpeta = "/Med_2025-2026/Reportes_Edit/Reporte_4.4/2025/11. Noviembre/BMT3-03-T80/DATOS"
archivo = 'msj24_validados_realt_2025110620_2025113023.pkl'
ruta_BMT3_3 = os.path.join(carpeta, archivo)

carpeta = "/Med_2025-2026/Reportes_Edit/Reporte_2.4/2025/11. Noviembre/BOT2-01-T20/DATOS"
archivo = 'msj4_validados_realt_2025111919_2025113023.pkl'
ruta_BOT2_1 = os.path.join(carpeta, archivo)

carpeta = "/Med_2025-2026/Reportes_Edit/Reporte_2.4/2025/11. Noviembre/BOT2-02-T20/DATOS"
archivo = 'msj4_validados_realt_2025111821_2025113023.pkl'
ruta_BOT2_2 = os.path.join(carpeta, archivo)


data_BMT3_3 = leer_datos_de_corrientes_pickle(ruta_BMT3_3)
# data_BOT2_1 = leer_datos_de_corrientes_pickle(ruta_BOT2_1)
data_BOT2_2 = leer_datos_de_corrientes_pickle(ruta_BOT2_2)

[df_BMT3_3,prof] = crear_dataframe_corrientes_desde_pickle(data_BMT3_3)
# [df_BOT2_1,prof] = crear_dataframe_corrientes_desde_pickle(data_BOT2_1)
# [df_BOT2_2,prof] = crear_dataframe_corrientes_desde_pickle(data_BOT2_2)

# df = pd.DataFrame()
# df["tspan"] = pd.date_range(start='2025-11-01 00:00', end='2025-11-30 23:00', freq='h')
# df_BOT2_2["Salinidad_MCT"]


# df = create_sample_data(ndays=10000)
# # grafico = GraCorrector(df)
# gra = GraficoInteractivo(df)
# gra.start_app()

# Crear la ventana principal
# print(df['temperatura'].dtype)

app = InteractivePlotterTk(df_BMT3_3)

# Iniciar el bucle de la aplicación
app.root.mainloop()
   
# NOTAS PENDIENTES:
# - Arreglar que al eliminar puntos para que no tenga límite el historial de deshacer
# - Arreglar para que solo se grafiquen las columnas elegidas por el usuario
# - Agregar una función que grafique las variables de Rap y Dir --> sería algo como que df.iloc[idx,col][prof]
# - Arreglar el caso de cuando el usuario elimina puntos de Rap o Dir colocar U y V como nans --> df.iloc[idx,col][prof] = np.nan
# - Agregar la funcionalidad de guardar el DataFrame corregido en un archivo .csv o .xlsx, pkl
# - Agregar la funcionalidad de devolver puntos eliminados (no deshacer la última acción, sino devolver puntos específicos)
import pandas as pd

def get_excel_column(df: pd.DataFrame, nombre_del_archivo_netcdf: str) -> int:
    fecha_excel = None
    fecha_inicial = None
    
    fecha_inicial_str = nombre_del_archivo_netcdf.split("-")[-2]
    fecha_inicial = pd.to_datetime(fecha_inicial_str, format="%Y%m%d")
    fecha_inicial = fecha_inicial.replace(hour=0, minute=0, second=0, microsecond=0)
    
    number_of_attempts = 7
    retry_number = 0
    while retry_number < number_of_attempts:
        for icol in range(1, len(df.columns)):
            fecha_excel = pd.to_datetime(df.iloc[0,icol], format = "%d/%m/%Y %H:%M")
            fecha_excel = fecha_excel.replace(hour=0, minute=0, second=0, microsecond=0)
            if fecha_excel == fecha_inicial:
                return icol + 1 # Se suma 1 porque las columnas en Excel comienzan en 1, no en 0; y el dataframe si inicia en 0.

        error_msg = f"No se encontró la fecha {fecha_inicial.strftime('%Y-%m-%d')} en el archivo Excel. Se intentará con la fecha del día anterior."
        fecha_inicial -= pd.Timedelta(days=1)
        retry_number += 1
        print(error_msg)
  
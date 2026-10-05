import numpy as np
import datetime

# FECHAS DE MATLAB A PYTHON en formato datetime
def datenum_to_datetime(datenum):
    """Lee un array en formato datenum de matlab (numeros de orden 7XXXXX) y los cambia al formato datetime de python.
    Por lo general los datos datenum vienen desde un archivo netCDF generado por matlab por lo que pueden venir como un Masked Array.
    Esta Funcion utiliza las librerías datetime y numpy para hacer la conversión de fechas.
    ***********
    by BelloDev
    agregado 2025/04/06
    ultima revision 2025/04/06
    ***********
    """
    # Primero convierte el maskedArray en un array normal de python
    if isinstance(datenum, np.ma.MaskedArray):
        fechas = np.array(datenum.filled(np.nan))
    else:
        fechas = np.array(datenum)

    # Lista para almacenar las fechas convertidas
    fechas_convertidas = []
    
    for idatenum in fechas.flatten():
         # Conversion de idatenum a un valor escalar
        idatenum = float(idatenum)

        # Convierte un número datenum de MATLAB a datetime de Python
        fecha = datetime.datetime.fromordinal(int(idatenum)) + datetime.timedelta(days=idatenum % 1) - datetime.timedelta(days=366)
        #fechas_convertidas.append(fecha)

        # Redondear al minuto más cercano
        fecha = fecha.replace(microsecond=0)
        if fecha.second >= 30:
            fecha += datetime.timedelta(minutes=1)
        
        fecha = fecha.replace(second=0)
        fechas_convertidas.append(fecha)

    # Retorna las fechas convertidas como un array de numpy
    return np.array(fechas_convertidas)
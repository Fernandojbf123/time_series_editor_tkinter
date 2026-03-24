import numpy as np
import datetime

# FECHAS DE MATLAB A PYTHON en formato datetime
def datenum_to_datetime(datenum):
    """
    Descripción:
        Convierte un array en formato datenum de MATLAB a objetos datetime de Python, redondeando al minuto más cercano y manejando MaskedArray.

    Parámetros:
        datenum (array-like): Array de números datenum (puede ser MaskedArray).

    Retorna:
        np.ndarray: Array de objetos datetime convertidos y redondeados al minuto.

    Ejemplo:
        >>> datenum_to_datetime([738000.501, 738001.499])

    Categoría:
        Funciones-Comunes

    Funciones auxiliares:
        np.array, datetime.datetime.fromordinal, datetime.timedelta
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
        # Redondear al minuto más cercano
        fecha = fecha.replace(microsecond=0)
        if fecha.second >= 30:
            fecha += datetime.timedelta(minutes=1)
        fecha = fecha.replace(second=0)
        fechas_convertidas.append(fecha)
    # Retorna las fechas convertidas como un array de numpy
    return np.array(fechas_convertidas)
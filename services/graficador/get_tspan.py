import numpy as np
import pandas as pd


def get_tspan(linea):
    tmp_day = str(int(linea.split(",")[2])+20000000)
    year = int(tmp_day[0:4])
    month = int(tmp_day[4:6])
    day = int(tmp_day[6:8])
    hour = int(np.floor(int(linea.split(",")[3])/10000))
    tspan = pd.Timestamp(year=year, month=month, day=day, hour=hour)    
    return tspan
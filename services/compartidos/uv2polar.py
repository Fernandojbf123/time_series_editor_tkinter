import numpy as np

def uv2polar(u, v):
    # Magnitud
    spd = np.hypot(u, v)
    # Dirección en radianes (como MATLAB: cart2pol(v, u))
    dir_rad = np.arctan2(u, v)
    # Ajuste de ángulo negativo
    dir_rad = np.where(dir_rad < 0, dir_rad + 2 * np.pi, dir_rad)
    # Convertir a grados
    dir_deg = np.degrees(dir_rad)
    return dir_deg, spd
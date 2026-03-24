import numpy as np
def polar2uv(direccion, rapidez):
    
    """
    
    Descripción:
        Convierte datos en coordenadas polares (dirección en grados y rapidez en m/s) a componentes cartesianas 
        `u` y `v`, útiles para representar vectores de viento, corriente u oleaje en el plano XY.

    Parámetros:
        direccion (array-like or float):
            Dirección en grados (°), donde 0° representa el norte y los ángulos aumentan en sentido horario 
            (convención meteorológica u oceanográfica).

        rapidez (array-like or float):
            Magnitud del vector (e.g., velocidad en m/s).

    Retorna:
        tuple (u, v):
            Componentes cartesianas del vector:
                - u (float or np.ndarray): Componente en el eje X (este-oeste).
                - v (float or np.ndarray): Componente en el eje Y (norte-sur).

    Ejemplo:
        >>> u, v = polar2uv(90, 2.0)
        >>> print(u, v)
        2.0 0.0

    Categoría:
        Funciones-Comunes


    """
   
    rad = np.radians(direccion)
    # rad = np.deg2rad(direccion)
    u = rapidez * np.sin(rad)
    v = rapidez * np.cos(rad)
    
    return u, v
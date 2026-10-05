def obtener_boyas(eleccion: int | list[int], estado: str = "validado"):
    """
    opciones:
    estado = "validado" (por defecto), "crudo" o "todos"

    - crudo: devuelve solo los estados crudos
    - validado: devuelve solo los estados validados
    - todos: devuelve todos los estados disponibles
    
    01: "BOT1-01-T80"
    
    02: "BOT1-03-T50"
    
    03: "BOT1-04-T80"
    
    04: "BOT1-05-T50"
    
    05: "BOT1-06-T50"
    
    06: "BOT1-07-T80"
    
    07: "BOT1-09-T50"
    
    08: "BOT1-10-T40"
    
    09: "BOT1-11-T100"
    
    10: "BOT2-01-T20"
    
    11: "BOT2-02-T20"
    
    12: "BMT2-01-T20"
    
    13: "BMT3-03-T80"
    
    14: "BMT3-04-T45"
    
    15: "BMT3-10-T45"
    
    16: "BMT3-10-T45"
    
    17: "BMT3-11-T1000"

    """


    boyas = {
        1: {"name": "BOT1-01-T80", "estados": ["crudo","validado"]}, 
        2: {"name": "BOT1-03-T50", "estados": ["crudo","validado"]},
        3: {"name": "BOT1-04-T80", "estados": ["crudo","validado"]},
        4: {"name": "BOT1-05-T50", "estados": ["crudo","validado"]},
        5: {"name": "BOT1-06-T50", "estados": ["crudo","validado"]},
        6: {"name": "BOT1-07-T80", "estados": ["crudo","validado"]},
        7: {"name": "BOT1-09-T50", "estados": ["crudo","validado"]},
        8: {"name": "BOT1-10-T40", "estados": ["crudo","validado"]},
        9: {"name": "BOT1-11-T100", "estados": ["crudo","validado"]},
        10: {"name": "BOT2-01-T20", "estados": ["crudo","validado"]},
        11: {"name": "BOT2-02-T20", "estados": ["crudo","validado"]},
        12: {"name": "BMT2-01-T20", "estados": ["crudo","validado"]},
        13: {"name": "BMT3-03-T80", "estados" : ["crudo","validado"]},
        14: {"name": "BMT3-04-T45", "estados": ["crudo","validado"]},
        15: {"name": "BMT3-10-T45", "estados": ["crudo","validado"]},
        16: {"name": "BMT3-10-T45", "estados": ["crudo","validado"]},
        17: {"name": "BMT3-11-T1000", "estados": ["crudo","validado"]},
    }
    
    if estado == "crudo":
        index = [0];
    elif estado == "validado":
        index = [1];
    elif estado == "todos":
        index = [0,1];
    else:
        raise ValueError(f"Estado desconocido: {estado}")
    
    elegidas = {}
    if isinstance(eleccion, int):
        boya = boyas.get(eleccion, None)
        nombre = boya.get("name",None)
        estados = boya.get("estados",None)
        elegidas[nombre] = [estados[i] for i in index]
         
    if isinstance(eleccion, list):
        for e in eleccion:
            boya = boyas.get(e, None)
            if boya:
                nombre = boya.get("name",None)
                estados = boya.get("estados",None)
                elegidas[nombre] = [estados[i] for i in index]
    
    return elegidas
       
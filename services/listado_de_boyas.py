def obtener_boyas(eleccion: int | list[int], estado: str = "validado"):

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
        index = 0;
    elif estado == "validado":
        index = 1;
    elif estado == "todos":
        index = slice(0,2);
    else:
        raise ValueError(f"Estado desconocido: {estado}")
    
    elegidas = {}
    if isinstance(eleccion, int):
        boya = boyas.get(eleccion, None)
        nombre = boya.get("name",None)
        estados = boya.get("estados",None)
        elegidas[nombre] = estados[index]
         
    if isinstance(eleccion, list):
        for e in eleccion:
            boya = boyas.get(e, None)
            if boya:
                nombre = boya.get("name",None)
                estados = boya.get("estados",None)
                elegidas[nombre] = estados[index]
    
    return elegidas
       
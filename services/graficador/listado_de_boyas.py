def obtener_boyas(eleccion: str | list[str], estado: str = "validado"):
    """
    opciones:
    estado = "validado" (por defecto), "crudo" o "todos"

    - crudo: devuelve solo los estados crudos
    - validado: devuelve solo los estados validados
    - todos: devuelve todos los estados disponibles
 
    """

    boyas = {
        "BOT1-01-T80": {"name": "BOT1-01-T80", "estados": ["crudo","validado"]}, 
        "BOT1-03-T50": {"name": "BOT1-03-T50", "estados": ["crudo","validado"]},
        "BOT1-04-T80": {"name": "BOT1-04-T80", "estados": ["crudo","validado"]},
        "BOT1-05-T50": {"name": "BOT1-05-T50", "estados": ["crudo","validado"]},
        "BOT1-06-T50": {"name": "BOT1-06-T50", "estados": ["crudo","validado"]},
        "BOT1-07-T80": {"name": "BOT1-07-T80", "estados": ["crudo","validado"]},
        "BOT1-09-T50": {"name": "BOT1-09-T50", "estados": ["crudo","validado"]},
        "BOT1-10-T40": {"name": "BOT1-10-T40", "estados": ["crudo","validado"]},
        "BOT1-11-T100": {"name": "BOT1-11-T100", "estados": ["crudo","validado"]},
        "BOT2-01-T20": {"name": "BOT2-01-T20", "estados": ["crudo","validado"]},
        "BOT2-02-T20": {"name": "BOT2-02-T20", "estados": ["crudo","validado"]},
        "BMT2-01-T20": {"name": "BMT2-01-T20", "estados": ["crudo","validado"]},
        "BMT3-03-T80": {"name": "BMT3-03-T80", "estados" : ["crudo","validado"]},
        "BMT3-04-T45": {"name": "BMT3-04-T45", "estados": ["crudo","validado"]},
        "BMT3-10-T45": {"name": "BMT3-10-T45", "estados": ["crudo","validado"]},
        "BMT3-11-T1000": {"name": "BMT3-11-T1000", "estados": ["crudo","validado"]},
    }
    
    if estado == "crudo":
        index = [0];
    elif estado == "validado":
        index = [1];
    elif estado == "todos":
        index = [0,1];
    else:
        raise ValueError(f"Estado desconocido: {estado}")
    
    boyas_elegidas = {}
    if isinstance(eleccion, str):
        boya = boyas.get(eleccion, None)
        if boya is None:
            raise ValueError(f"Boyas desconocida: {eleccion}")
        
        name = boya.get("name",None)
        estados = boya.get("estados",None)
        if estados is None:
            raise ValueError(f"Estados no encontrados para la boya: {eleccion}. Las opciones diponibles son: 'Crudo', 'Validado', 'Todos'")
        boyas_elegidas[eleccion] = [estados[i] for i in index]
         
    if isinstance(eleccion, list):
        for e in eleccion:
            boya = boyas.get(e, None)
            if boya is None:
                raise ValueError(f"Boyas desconocida: {e}")
            
            name = boya.get("name",None)
            estados = boya.get("estados",None)
            if estados is None:
                        raise ValueError(f"Estados no encontrados para la boya: {eleccion}. Las opciones diponibles son: 'Crudo', 'Validado', 'Todos'")
            boyas_elegidas[e] = [estados[i] for i in index]
    
    return boyas_elegidas
       
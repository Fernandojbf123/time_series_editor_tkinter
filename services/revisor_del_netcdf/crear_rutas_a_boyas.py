import os
import dotenv

dotenv.load_dotenv()
ruta_nas = os.getenv("RUTA_NAS", "")


def ruta_a_bots1() -> dict:
    oleaje = "OLEAJE\\VALIDADOS"
    corrientes = "CORRIENTES\\VALIDADOS"
    ruta_boya = {
        "oleaje": oleaje,
        "corrientes": corrientes,
        "reporte": "Reporte_1.2"
    }
    return ruta_boya

def ruta_bots2() -> dict:
    oleaje = "OLEAJE\\VALIDADOS"
    corrientes = "CORRIENTES\\VALIDADOS"
    mct = "TEMP_SAL\\VALIDADOS"
    ruta_boya = {
        "oleaje": oleaje,
        "corrientes": corrientes,
        "mct": mct,
        "reporte": "Reporte_2.2"
    }
    return ruta_boya

def ruta_bmt2() -> dict:
    meteorologicos = "METEOROLOGICOS\\VALIDADOS"
    oleaje = "OCEANOGRAFICOS\\OLEAJE\\VALIDADOS"
    corrientes = "OCEANOGRAFICOS\\CORRIENTES\\VALIDADOS"
    mct = "OCEANOGRAFICOS\\TEMP_SAL\\VALIDADOS"
    ruta_boya = {
        "meteorologicos": meteorologicos,
        "oleaje": oleaje,
        "corrientes": corrientes,
        "mct": mct,
        "reporte": "Reporte_3.2"
    }
    return ruta_boya

def ruta_bmt3() -> dict:
    meteorologicos = "METEOROLOGICOS\\VALIDADOS"
    oleaje = "OCEANOGRAFICOS\\OLEAJE\\VALIDADOS"
    corrientes = "OCEANOGRAFICOS\\CORRIENTES\\VALIDADOS"
    mct = "OCEANOGRAFICOS\\TEMP_SAL\\VALIDADOS"
    ruta_boya = {
        "meteorologicos": meteorologicos,
        "oleaje": oleaje,
        "corrientes": corrientes,
        "mct": mct,
        "reporte": "Reporte_4.2"
    }
    return ruta_boya


def crea_ruta_a_datos_de_boya(boya:str, anio:str, mes:str, tipo:str) -> str:
    """ 
    boya = "BOT1-01-T80"
    anio = "2026"
    mes = "03. Marzo"
    tipo = "oleaje" # opciones: "oleaje", "corrientes", "mct", "meteo"
    """
    
    if boya.split("-")[0].lower() == "bot1":
        ruta_boya = ruta_a_bots1()
    elif boya.split("-")[0].lower() == "bot2":
        ruta_boya = ruta_bots2()
    elif boya.split("-")[0].lower() == "bmt2":
        ruta_boya = ruta_bmt2()
    elif boya.split("-")[0].lower() == "bmt3":
        ruta_boya = ruta_bmt3()
    else: 
        raise ValueError(f"Se desconoce el tipo de boya {boya}. No se puede crear la ruta.")
     
    ruta = os.path.join(f"\\\\{ruta_nas}", "Med_2025-2026", "Reportes_Edit", ruta_boya["reporte"], anio, mes, boya, "RECUPERACION", boya)
    if tipo == "corrientes":
        ruta_final = os.path.join(ruta, ruta_boya["corrientes"])
    elif tipo == "oleaje":
        ruta_final = os.path.join(ruta, ruta_boya["oleaje"])
    elif tipo == "mct":
        ruta_final = os.path.join(ruta, ruta_boya["mct"])
    elif tipo == "meteo":
        ruta_final = os.path.join(ruta, ruta_boya["meteorologicos"])
    else:
        raise ValueError(f"Se desconoce el tipo de dato {tipo}. No se puede crear la ruta.")
    
    return ruta_final
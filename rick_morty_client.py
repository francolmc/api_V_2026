import time
import requests
from models.recluta import Recluta

BASE_URL = "https://rickandmortyapi.com/api"
TIMEOUT = 5 # segundos
INTENTOS = 3 # intentos

class ReclutaNoEncontradoError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass

def _get(ruta):
    motivo = "No se pudo contactar al servicio"
    for intento in range(1, INTENTOS + 1):
        try:
            r = requests.get(BASE_URL + ruta, timeout=TIMEOUT)
            if r.status_code != 429 and r.status_code < 500:
                return r
            motivo = "El servicio esta ocupado, intente mas tarde"
        except requests.exceptions.Timeout:
            motivo = "El servicio no esta disponible"
        except requests.exceptions.ConnectionError:
            motivo = "No hay conexion."
        if intento < INTENTOS:
            print(f"No hay conexion, reintentado en {intento} segundos.")
            time.sleep(intento) # pausa creciente: 1s, 2s
    raise ServicioNoDisponibleError(motivo) from None

def obtener_recluta(id_api):
    if not isinstance(id_api, int) or id_api < 1:
        raise ValueError("El id debe un entero positivo")
    respuesta = _get(f"/character/{id_api}")
    if respuesta.status_code == 404:
        raise ReclutaNoEncontradoError(id_api)
    if not respuesta.ok:
        raise ServicioNoDisponibleError("El servicio no retorno la respuesta") from None
    try:
        return Recluta.desde_dict(respuesta.json())
    except ValueError:
        raise ServicioNoDisponibleError("La respuesta no es valida") from None
    
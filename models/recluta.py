class DatosInvalidosError(Exception):
    pass

class Recluta:
    def __init__(self, id_api, nombre, estado, especie, origen):
        self.id_api = id_api
        self.nombre = nombre
        self.estado = estado
        self.especie = especie
        self.origen = origen

    @classmethod
    def desde_dict(cls, d):
        try:
            return cls(d["id"], d["name"], d["status"], d["species"], d["origin"]["name"])
        except (KeyError, TypeError):
            raise DatosInvalidosError(
                "La respuesta no tiene el forma esperado"
                ) from None

    def __str__(self):
        return f"#{self.id_api} {self.nombre} - {self.estado}, {self.especie} ({self.origen})"
from abc import ABC, abstractmethod

# 1. Excepciones personalizadas
class DatoInvalidoError(Exception):
    """Se lanza cuando un dato ingresado no cumple con las reglas."""
    pass

class ClienteNoEncontradoError(Exception):
    """Se lanza cuando se busca un cliente que no existe en el sistema."""
    pass

# 2. Clase abstracta base para todas las entidades del sistema
class EntidadBase(ABC):
    @abstractmethod
    def mostrar_info(self) -> str:
        """Método obligatorio que deben implementar las clases hijas."""
     pass
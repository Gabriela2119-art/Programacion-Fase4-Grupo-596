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

# 3. Clase Cliente con encapsulación estricta
class Cliente(EntidadBase):
    def __init__(self, nombre: str, documento: str, correo: str):
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    # --- Propiedad y validación para Nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 letras y no estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad y validación para Documento ---
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        if not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) < 5:
            raise DatoInvalidoError("El documento debe contener solo números (mínimo 5 dígitos).")
        self._documento = valor.strip()

    # --- Propiedad y validación para Correo ---
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip()

    def mostrar_info(self) -> str:
        return f"Cliente: {self._nombre} | Doc: {self._documento} | Correo: {self._correo}"

        # 4. Funciones de prueba iniciales
def ejecutar_pruebas_cliente():
    print("--- INICIANDO PRUEBAS DE CLIENTE ---")
    
    # Caso válido 1
    try:
        c1 = Cliente("Laura Gómez", "10203040", "laura@correo.com")
        print("[OK] Cliente creado:", c1.mostrar_info())
    except DatoInvalidoError as e:
        print("[ERROR INESPERADO]", e)

    # Caso inválido 1: Nombre vacío
    try:
        c2 = Cliente("", "98765432", "carlos@correo.com")
    except DatoInvalidoError as e:
        print("[OK - Error capturado correctamente]:", e)

    # Caso inválido 2: Documento con letras
    try:
        c3 = Cliente("Andrés Pérez", "123ABC", "andres@correo.com")
    except DatoInvalidoError as e:
        print("[OK - Error capturado correctamente]:", e)

    # Caso inválido 3: Correo sin arroba
    try:
        c4 = Cliente("Sofía Ruiz", "55667788", "sofiacorreo.com")
    except DatoInvalidoError as e:
        print("[OK - Error capturado correctamente]:", e)

if __name__ == "__main__":
    ejecutar_pruebas_cliente()

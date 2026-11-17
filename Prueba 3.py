from abc import ABC, abstractmethod
from datetime import datetime
import os

# ==========================================
# 1. EXCEPCIONES Y CLASE BASE
# ==========================================

class DatoInvalidoError(Exception):
    """Se lanza cuando un dato ingresado no cumple con las reglas."""
    pass

class ClienteNoEncontradoError(Exception):
    """Se lanza cuando se busca un cliente que no existe en el sistema."""
    pass

class EntidadBase(ABC):
    @abstractmethod
    def mostrar_info(self) -> str:
        """Método obligatorio que deben implementar las clases hijas."""
        pass


# ==========================================
# 2. MÓDULO CLIENTE
# ==========================================

class Cliente(EntidadBase):
    """Representa a un cliente del sistema Software FJ."""
    
    def __init__(self, nombre: str, documento: str, correo: str):
        self._nombre = nombre
        self._documento = documento
        self._correo = correo
        self.validar_datos()

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def documento(self) -> str:
        return self._documento

    @property
    def correo(self) -> str:
        return self._correo

    def validar_datos(self) -> None:
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise DatoInvalidoError("El nombre del cliente no puede estar vacío.")
        if not isinstance(self._documento, str) or not self._documento.strip():
            raise DatoInvalidoError("El documento del cliente no puede estar vacío.")
        if not isinstance(self._correo, str) or "@" not in self._correo:
            raise DatoInvalidoError("El correo electrónico no es válido.")
        self._nombre = self._nombre.strip()
        self._documento = self._documento.strip()
        self._correo = self._correo.strip().lower()

    def mostrar_info(self) -> str:
        return f"Cliente: {self.nombre} | Documento: {self.documento} | Correo: {self.correo}"


# ==========================================
# 3. MÓDULO SERVICIOS
# ==========================================

class Servicio(EntidadBase, ABC):
    """Clase abstracta que representa un servicio ofrecido por Software FJ."""

    def __init__(self, nombre_servicio: str, tarifa_base: float):
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = tarifa_base
        self._validar_datos_base()

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    def _validar_datos_base(self) -> None:
        if not isinstance(self._nombre_servicio, str) or not self._nombre_servicio.strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        if isinstance(self._tarifa_base, bool) or not isinstance(self._tarifa_base, (int, float)):
            raise DatoInvalidoError("La tarifa base debe ser un valor numérico.")
        if self._tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")
        self._tarifa_base = float(self._tarifa_base)

    @staticmethod
    def _validar_calculo(duracion: int, descuento: float, impuesto: float) -> None:
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise DatoInvalidoError("La duración debe ser un número entero mayor que cero.")
        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("El descuento debe estar entre 0.0 y 1.0.")
        if impuesto < 0:
            raise DatoInvalidoError("El impuesto no puede ser negativo.")

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    @abstractmethod
    def validar_parametros(self) -> None:
        pass

    def mostrar_info(self) -> str:
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio para reservar una sala por horas."""
    def __init__(self, nombre_servicio: str, tarifa_base: float, capacidad: int = 10, costo_limpieza: float = 0.0):
        super().__init__(nombre_servicio, tarifa_base)
        self._capacidad = capacidad
        self._costo_limpieza = costo_limpieza
        self.validar_parametros()

    def validar_parametros(self) -> None:
        self._validar_datos_base()
        if isinstance(self._capacidad, bool) or not isinstance(self._capacidad, int) or self._capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero mayor a cero.")
        if isinstance(self._costo_limpieza, bool) or not isinstance(self._costo_limpieza, (int, float)) or self._costo_limpieza < 0:
            raise DatoInvalidoError("El costo de limpieza no puede ser negativo.")
        self._costo_limpieza = float(self._costo_limpieza)

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        self._validar_calculo(duracion, descuento, impuesto)
        subtotal = (self.tarifa_base * duracion) + self._costo_limpieza
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir_servicio(self) -> str:
        return f"Reserva de sala: {self.nombre_servicio}. Capacidad: {self._capacidad} personas. Tarifa/hora: ${self.tarifa_base:,.2f}"


# ==========================================
# 4. MÓDULO RESERVA Y LOGS (CON CREACIÓN AUTOMÁTICA DEL TXT)
# ==========================================

class GestorLogs:
    """Clase utilitaria para el registro centralizado de eventos y errores."""
    @staticmethod
    def registrar_evento(mensaje: str, nivel: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"
        
        # Garantiza que el archivo 'logs.txt' se cree exactamente en la carpeta actual del script
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(dir_actual, "logs.txt")
        
        try:
            with open(ruta_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea_log)
        except Exception as e:
            print(f"Error crítico al escribir logs: {e}")


class Reserva:
    """Clase que integra cliente, servicio, duración y estados."""
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: int):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"

    def confirmar(self) -> float:
        if self.duracion <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser mayor a cero.")
        self.servicio.validar_parametros()
        costo_total = self.servicio.calcular_costo(self.duracion)
        self.estado = "CONFIRMADA"
        return costo_total

    def procesar(self) -> None:
        try:
            GestorLogs.registrar_evento(f"Iniciando procesamiento. Cliente: {self.cliente.nombre} | Servicio: {type(self.servicio).__name__}", "INFO")
            costo = self.confirmar()
        except DatoInvalidoError as e:
            self.estado = "CANCELADA"
            GestorLogs.registrar_evento(f"Error de validación: {str(e)}", "ERROR")
            raise
        except Exception as e:
            self.estado = "CANCELADA"
            GestorLogs.registrar_evento(f"Error inesperado: {str(e)}", "CRITICAL")
            raise
        else:
            GestorLogs.registrar_evento(f"Reserva con éxito. Estado: {self.estado}. Costo: ${costo:,.2f}", "INFO")
        finally:
            GestorLogs.registrar_evento(f"Cierre de ciclo para {self.cliente.nombre}. Estado final: {self.estado}.", "INFO")


# ==========================================
# 5. BLOQUE DE PRUEBAS PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("=== PROBANDO EL SISTEMA UNIFICADO SOFTWARE FJ ===")
    try:
        # Creamos un cliente
        cli = Cliente("Ana Gómez", "10987654", "ana@email.com")
        print(f"[OK] {cli.mostrar_info()}")

        # Creamos un servicio de sala
        sala = ReservaSala("Sala Ejecutiva", 50000, capacidad=10, costo_limpieza=15000)
        print(f"[OK] {sala.describir_servicio()}")

        # Procesamos la reserva (Esto creará o actualizará automáticamente el archivo logs.txt en tu carpeta)
        reserva = Reserva(cliente=cli, servicio=sala, duracion=3)
        reserva.procesar()

        print(f"\n¡Prueba ejecutada con éxito! Estado de la reserva: {reserva.estado}")
        print("¡Revisa tu carpeta 'FJ': ya se creó el archivo 'logs.txt' con el registro!")

    except Exception as e:
        print(f"\n[ERROR CONTROLADO]: {e}")
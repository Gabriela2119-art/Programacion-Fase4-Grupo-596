from abc import ABC, abstractmethod
from datetime import datetime
import os

# ==========================================
# 1. EXCEPCIONES PERSONALIZADAS
# ==========================================

class DatoInvalidoError(Exception):
    """Se lanza cuando un dato ingresado no cumple con las reglas."""
    pass


class ClienteNoEncontradoError(Exception):
    """Se lanza cuando se busca un cliente que no existe en el sistema."""
    pass


# ==========================================
# 2. CLASE ABSTRACTA BASE
# ==========================================

class EntidadBase(ABC):
    @abstractmethod
    def mostrar_info(self) -> str:
        """Método obligatorio que deben implementar las clases hijas."""
        pass


# ==========================================
# 3. CLASE CLIENTE CON ENCAPSULACIÓN ESTRICTA
# ==========================================

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


# ==========================================
# 4. MÓDULO DE SERVICIOS (ABSTRACCIÓN, HERENCIA Y POLIMORFISMO)
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
        """Valida los atributos comunes a todos los servicios."""
        if not isinstance(self._nombre_servicio, str) or not self._nombre_servicio.strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")

        if isinstance(self._tarifa_base, bool) or not isinstance(self._tarifa_base, (int, float)):
            raise DatoInvalidoError("La tarifa base debe ser un valor numérico.")

        if self._tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")

        self._nombre_servicio = self._nombre_servicio.strip()
        self._tarifa_base = float(self._tarifa_base)

    @staticmethod
    def _validar_calculo(duracion: int, descuento: float, impuesto: float) -> None:
        """Valida los parámetros usados para calcular cualquier servicio."""
        if isinstance(duracion, bool) or not isinstance(duracion, int):
            raise DatoInvalidoError("La duración debe ser un número entero.")
        if duracion <= 0:
            raise DatoInvalidoError("La duración debe ser mayor que cero.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise DatoInvalidoError("El descuento debe ser numérico.")
        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("El descuento debe estar entre 0.0 y 1.0.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise DatoInvalidoError("El impuesto debe ser numérico.")
        if impuesto < 0:
            raise DatoInvalidoError("El impuesto no puede ser negativo.")

    @abstractmethod
    def calcular_costo(
        self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19
    ) -> float:
        """Calcula el valor total del servicio."""
        raise NotImplementedError

    @abstractmethod
    def describir_servicio(self) -> str:
        """Devuelve una descripción particular del servicio."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self) -> None:
        """Valida los parámetros particulares del servicio."""
        raise NotImplementedError

    def mostrar_info(self) -> str:
        """Implementa el método heredado de EntidadBase."""
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio para reservar una sala por horas."""

    def __init__(
        self,
        nombre_servicio: str,
        tarifa_base: float,
        capacidad: int = 10,
        costo_limpieza: float = 0.0,
    ):
        super().__init__(nombre_servicio, tarifa_base)
        self._capacidad = capacidad
        self._costo_limpieza = costo_limpieza
        self.validar_parametros()

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar_parametros(self) -> None:
        self._validar_datos_base()
        if isinstance(self._capacidad, bool) or not isinstance(self._capacidad, int):
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero.")
        if self._capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor que cero.")
        if isinstance(self._costo_limpieza, bool) or not isinstance(
            self._costo_limpieza, (int, float)
        ):
            raise DatoInvalidoError("El costo de limpieza debe ser numérico.")
        if self._costo_limpieza < 0:
            raise DatoInvalidoError("El costo de limpieza no puede ser negativo.")
        self._costo_limpieza = float(self._costo_limpieza)

    def calcular_costo(
        self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19
    ) -> float:
        self._validar_calculo(duracion, descuento, impuesto)
        subtotal = (self.tarifa_base * duracion) + self._costo_limpieza
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def describir_servicio(self) -> str:
        return (
            f"Reserva de sala: {self.nombre_servicio}. Capacidad: "
            f"{self.capacidad} personas. Tarifa por hora: ${self.tarifa_base:,.2f}."
        )


class AlquilerEquipo(Servicio):
    """Servicio para alquilar uno o varios equipos por horas."""

    def __init__(
        self,
        nombre_servicio: str,
        tarifa_base: float,
        cantidad_equipos: int = 1,
        seguro_por_equipo: float = 0.0,
    ):
        super().__init__(nombre_servicio, tarifa_base)
        self._cantidad_equipos = cantidad_equipos
        self._seguro_por_equipo = seguro_por_equipo
        self.validar_parametros()

    @property
    def cantidad_equipos(self) -> int:
        return self._cantidad_equipos

    def validar_parametros(self) -> None:
        self._validar_datos_base()
        if isinstance(self._cantidad_equipos, bool) or not isinstance(
            self._cantidad_equipos, int
        ):
            raise DatoInvalidoError("La cantidad de equipos debe ser un entero.")
        if self._cantidad_equipos <= 0:
            raise DatoInvalidoError("La cantidad de equipos debe ser mayor que cero.")
        if isinstance(self._seguro_por_equipo, bool) or not isinstance(
            self._seguro_por_equipo, (int, float)
        ):
            raise DatoInvalidoError("El seguro por equipo debe ser numérico.")
        if self._seguro_por_equipo < 0:
            raise DatoInvalidoError("El seguro por equipo no puede ser negativo.")
        self._seguro_por_equipo = float(self._seguro_por_equipo)

    def calcular_costo(
        self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19
    ) -> float:
        self._validar_calculo(duracion, descuento, impuesto)
        alquiler = self.tarifa_base * duracion * self.cantidad_equipos
        seguro = self._seguro_por_equipo * self.cantidad_equipos
        subtotal = alquiler + seguro
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def describir_servicio(self) -> str:
        return (
            f"Alquiler de equipo: {self.nombre_servicio}. Cantidad: "
            f"{self.cantidad_equipos}. Tarifa por equipo/hora: "
            f"${self.tarifa_base:,.2f}."
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría con nivel de especialización configurable."""

    FACTORES_NIVEL = {"BASICA": 1.0, "AVANZADA": 1.25, "EXPERTA": 1.50}

    def __init__(
        self,
        nombre_servicio: str,
        tarifa_base: float,
        nivel: str = "BASICA",
    ):
        super().__init__(nombre_servicio, tarifa_base)
        self._nivel = nivel.upper().strip() if isinstance(nivel, str) else nivel
        self.validar_parametros()

    @property
    def nivel(self) -> str:
        return self._nivel

    def validar_parametros(self) -> None:
        self._validar_datos_base()
        if not isinstance(self._nivel, str) or self._nivel not in self.FACTORES_NIVEL:
            niveles = ", ".join(self.FACTORES_NIVEL)
            raise DatoInvalidoError(f"El nivel debe ser uno de estos valores: {niveles}.")

    def calcular_costo(
        self, duracion: int, descuento: float = 0.0, impuesto: float = 0.19
    ) -> float:
        self._validar_calculo(duracion, descuento, impuesto)
        factor = self.FACTORES_NIVEL[self.nivel]
        subtotal = self.tarifa_base * duracion * factor
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def describir_servicio(self) -> str:
        return (
            f"Asesoría especializada: {self.nombre_servicio}. Nivel: "
            f"{self.nivel}. Tarifa base por hora: ${self.tarifa_base:,.2f}."
        )


# ==========================================
# 5. GESTOR DE LOGS Y RESERVAS
# ==========================================

class GestorLogs:
    """Clase utilitaria para el registro centralizado de eventos y errores en un archivo de texto."""
    
    @staticmethod
    def registrar_evento(mensaje: str, nivel: str = "INFO") -> None:
        """Registra un evento o error con marca temporal en el archivo logs.txt."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"
        
        # Garantiza que logs.txt se cree en la misma carpeta donde esté este script
        dir_actual = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        ruta_archivo = os.path.join(dir_actual, "logs.txt")
        
        try:
            with open(ruta_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea_log)
        except Exception as e:
            print(f"Error crítico al intentar escribir en el archivo de logs: {e}")


class Reserva:
    """Clase que integra cliente, servicio, duración y estados de la reserva."""
    
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: int):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"  # Inicia siempre en PENDIENTE

    def confirmar(self) -> float:
        """Valida los parámetros, calcula el costo del servicio y confirma la reserva."""
        if self.duracion <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser mayor a cero (0).")
        
        # Valida los parámetros propios del servicio
        self.servicio.validar_parametros()
        
        # Realiza el cálculo del costo usando el método polimórfico
        costo_total = self.servicio.calcular_costo(self.duracion)
        
        self.estado = "CONFIRMADA"
        return costo_total

    def cancelar(self) -> None:
        """Cambia el estado de la reserva a CANCELADA."""
        self.estado = "CANCELADA"
        GestorLogs.registrar_evento(
            f"Reserva cancelada para el cliente '{self.cliente.nombre}' (Documento: {self.cliente.documento}).", 
            "WARNING"
        )

    def procesar(self) -> None:
        """Ejecuta la reserva completa utilizando la estructura try / except / else / finally."""
        try:
            GestorLogs.registrar_evento(
                f"Iniciando procesamiento de reserva. Cliente: {self.cliente.nombre} | Servicio: {type(self.servicio).__name__}", 
                "INFO"
            )
            
            # Intenta confirmar la reserva y calcular costos
            costo = self.confirmar()
            
        except DatoInvalidoError as e:
            self.estado = "CANCELADA"
            GestorLogs.registrar_evento(f"Error de validación en reserva: {str(e)}", "ERROR")
            raise
        except Exception as e:
            self.estado = "CANCELADA"
            GestorLogs.registrar_evento(f"Error inesperado al procesar la reserva: {str(e)}", "CRITICAL")
            raise
        else:
            GestorLogs.registrar_evento(
                f"Reserva procesada con éxito. Estado: {self.estado}. Costo calculado: ${costo:,.2f}", 
                "INFO"
            )
        finally:
            GestorLogs.registrar_evento(
                f"Cierre de ciclo de procesamiento para el cliente {self.cliente.nombre}. Estado final de reserva: {self.estado}.", 
                "INFO"
            )


# ==========================================
# 6. BLOQUE DE PRUEBAS INTEGRALES
# ==========================================

def ejecutar_pruebas_sistema() -> None:
    print("==========================================================")
    print("   INICIANDO PRUEBAS INTEGRALES - SOFTWARE FJ (FASE 4)    ")
    print("==========================================================\n")

    # 1. Prueba de Clientes (Válido e Inválidos)
    print("--- 1. VALIDACIÓN DE CLIENTES ---")
    try:
        c1 = Cliente("Laura Gómez", "10203040", "laura@correo.com")
        print("[OK] Cliente creado:", c1.mostrar_info())
    except DatoInvalidoError as e:
        print("[ERROR INESPERADO]", e)

    try:
        Cliente("Ana", "123ABC", "correo_invalido")
    except DatoInvalidoError as e:
        print("[OK - Error capturado correctamente]:", e)

    # 2. Prueba de Servicios y Polimorfismo
    print("\n--- 2. VALIDACIÓN DE SERVICIOS ---")
    sala = ReservaSala("Sala de Juntas", 50000, capacidad=12, costo_limpieza=15000)
    equipo = AlquilerEquipo("Portátiles", 25000, cantidad_equipos=3, seguro_por_equipo=5000)
    asesoria = AsesoriaEspecializada("Ciberseguridad", 80000, nivel="EXPERTA")

    for serv in [sala, equipo, asesoria]:
        print("  ->", serv.describir_servicio())

    # 3. Procesamiento de Reservas y Generación de logs.txt
    print("\n--- 3. PROCESAMIENTO DE RESERVAS Y REGISTRO EN LOGS.TXT ---")
    try:
        reserva_valida = Reserva(cliente=c1, servicio=sala, duracion=3)
        reserva_valida.procesar()
        print(f"[OK] Reserva 1 procesada. Estado final: {reserva_valida.estado}")
    except Exception as e:
        print(f"[ERROR]: {e}")

    try:
        reserva_invalida = Reserva(cliente=c1, servicio=asesoria, duracion=0)
        reserva_invalida.procesar()
    except DatoInvalidoError as e:
        print(f"[OK - Error de duración capturado]: {e} | Estado final: {reserva_invalida.estado}")

    print("\n==========================================================")
    print("¡Ejecución finalizada! Se ha generado/actualizado 'logs.txt'")
    print("en la misma carpeta donde guardaste este archivo Python.")
    print("==========================================================")


if __name__ == "__main__":
    ejecutar_pruebas_sistema()

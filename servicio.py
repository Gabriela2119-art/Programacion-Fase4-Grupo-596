"""Módulo de servicios para Software FJ.

Define la clase abstracta Servicio y tres servicios especializados.
Incluye abstracción, herencia, polimorfismo, sobrescritura y manejo
controlado de datos inválidos.
"""

from abc import ABC, abstractmethod
from cliente import EntidadBase, DatoInvalidoError


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


def ejecutar_pruebas_servicios() -> None:
    """Ejecuta casos válidos e inválidos sin detener el programa."""
    pruebas = [
        (
            "Reserva de sala válida",
            lambda: ReservaSala("Sala de juntas", 50000, 12, 15000),
            3,
        ),
        (
            "Alquiler de equipos válido",
            lambda: AlquilerEquipo("Portátiles", 25000, 3, 5000),
            4,
        ),
        (
            "Asesoría válida con descuento",
            lambda: AsesoriaEspecializada("Ciberseguridad", 80000, "EXPERTA"),
            2,
        ),
        (
            "Servicio con tarifa inválida",
            lambda: ReservaSala("Sala pequeña", -10000),
            2,
        ),
        (
            "Equipo con cantidad inválida",
            lambda: AlquilerEquipo("Video beam", 30000, 0),
            2,
        ),
        (
            "Asesoría con nivel inválido",
            lambda: AsesoriaEspecializada("Bases de datos", 70000, "SUPER"),
            2,
        ),
    ]

    for numero, (descripcion, creador, duracion) in enumerate(pruebas, start=1):
        try:
            servicio = creador()
            descuento = 0.10 if numero == 3 else 0.0
            costo = servicio.calcular_costo(duracion, descuento=descuento)
        except DatoInvalidoError as error:
            print(f"Prueba {numero} - {descripcion}: ERROR CONTROLADO -> {error}")
        else:
            print(f"Prueba {numero} - {descripcion}: OK")
            print(f"  {servicio.describir_servicio()}")
            print(f"  Costo total: ${costo:,.2f}")
        finally:
            print("  Prueba finalizada.\n")


if __name__ == "__main__":
    ejecutar_pruebas_servicios()

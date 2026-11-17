from datetime import datetime
from cliente import Cliente, DatoInvalidoError
from servicio import Servicio

class GestorLogs:
    """Clase utilitaria para el registro centralizado de eventos y errores en un archivo de texto."""
    
    @staticmethod
    def registrar_evento(mensaje: str, nivel: str = "INFO") -> None:
        """Registra un evento o error con marca temporal en el archivo logs.txt."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"
        try:
            with open("logs.txt", "a", encoding="utf-8") as archivo:
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
import numpy as np

from Musicode.engine import SAMPLE_RATE
from Musicode.envolvente import Env
from Musicode.track import Track


# CLASE BASE
class Wave:
    def __init__(self, frecuencia: float, duracion: float, amplitud: float = 0.5, env: Env = None):
        # 1. VALIDACIONES ESTRICTAS
        if frecuencia <= 0:
            raise ValueError("Error en Wave: La frecuencia debe ser mayor a 0 Hz.")
        if duracion < 0:
            raise ValueError("Error en Wave: La duración no puede ser negativa.")
        if amplitud < 0:
            raise ValueError("Error en Wave: La amplitud no puede ser negativa.")

        self.frecuencia = frecuencia
        self.duracion = duracion
        self.amplitud = amplitud
        
        # 2. GENERACIÓN (Delega a las subclases)
        self.buffer = self._generar_forma_onda()
        
        if env:
            self.buffer = env.aplicar(self.buffer, self.duracion)

    def _generar_forma_onda(self) -> np.ndarray:
        """Este método DEBE ser sobrescrito por las clases hijas."""
        raise NotImplementedError("Esta es una clase base. Usa Sine, Square o Saw.")
        
    def __add__(self, otra_onda):
        """Suma (Mix) para acordes."""
        max_len = max(len(self.buffer), len(otra_onda.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otra_onda.buffer, (0, max_len - len(otra_onda.buffer)))
        
        nueva_duracion = max_len / SAMPLE_RATE

        suma = buf1 + buf2
        suma_segura = np.clip(suma, -1.0, 1.0)

        
        # SOLUCIÓN: Devolvemos un objeto MixedWave que recibe directamente el buffer sumado
        return MixedWave(suma_segura, nueva_duracion)
    def __mul__(self, factor: float):
        """Modula la amplitud (volumen) de la onda."""
        if not isinstance(factor, (int, float)):
            raise TypeError("Error: Solo se puede multiplicar la onda por un número.")
            
        # Multiplicamos el buffer por el factor de volumen
        buffer_modulado = self.buffer * factor
        
        # Reutilizamos el escudo anticlipping por si el usuario multiplica por un número mayor a 1.0
        buffer_seguro = np.clip(buffer_modulado, -1.0, 1.0)
        
        # Devolvemos un MixedWave para mantener la inmutabilidad perfecta
        return MixedWave(buffer_seguro, self.duracion)
    # Esto permite que la multiplicación funcione al revés (ej. 0.5 * onda)
    __rmul__ = __mul__

    def __rshift__(self, otro):
        """Secuenciación de Tracks."""
        nuevo_track = Track()
        nuevo_track.agregar(self)
        nuevo_track.agregar(otro)
        return nuevo_track


# LOS SINTETIZADORES REALES (Subclases)
class Sine(Wave):
    def _generar_forma_onda(self) -> np.ndarray:
        total_samples = int(SAMPLE_RATE * self.duracion)
        t = np.linspace(0, self.duracion, total_samples, endpoint=False)
        onda = self.amplitud * np.sin(2 * np.pi * self.frecuencia * t)
        return onda.astype(np.float32)

class Square(Wave):
    def _generar_forma_onda(self) -> np.ndarray:
        total_samples = int(SAMPLE_RATE * self.duracion)
        t = np.linspace(0, self.duracion, total_samples, endpoint=False)
        
        # Calculamos la onda base
        seno = np.sin(2 * np.pi * self.frecuencia * t)
        
        # SOLUCIÓN: Si es mayor o IGUAL a cero, asigna 1.0. Si es menor, asigna -1.0
        # Esto elimina el "0" del centro por completo.
        onda = self.amplitud * np.where(seno >= 0, 1.0, -1.0)
        
        return onda.astype(np.float32)

class Saw(Wave):
    def _generar_forma_onda(self) -> np.ndarray:
        total_samples = int(SAMPLE_RATE * self.duracion)
        t = np.linspace(0, self.duracion, total_samples, endpoint=False)
        
        # (t * freq) % 1 genera una rampa de 0 a 1. 
        # Multiplicar por 2 y restar 1 centra la onda entre -1 y 1.
        onda = self.amplitud * (2.0 * ((t * self.frecuencia) % 1.0) - 1.0)
        return onda.astype(np.float32)


# CONTENEDORES ESPECIALES
class MixedWave(Wave):
    """Contenedor especial para ondas que han sido sumadas o modificadas."""
    def __init__(self, buffer: np.ndarray, duracion: float):
        # Nos saltamos las validaciones de frecuencia de la clase base 
        # porque esta onda ya está pre-calculada.
        self.frecuencia = 0
        self.duracion = duracion
        self.amplitud = 1.0
        self.buffer = buffer

    def _generar_forma_onda(self) -> np.ndarray:
        # Solo lo ponemos para cumplir la regla estricta de la clase base,
        # pero en realidad usamos el buffer que recibimos en el __init__.
        return self.buffer
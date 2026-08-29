import numpy as np
from Musicode.envolvente import Env
from Musicode.track import Track
from Musicode.engine import SAMPLE_RATE

#?ACTUALIZACIÓN DE LA ONDA (Wave)
class Wave:
    def __init__(self, frecuencia: float, duracion: float, amplitud: float = 0.5, env: Env = None):
        self.frecuencia = frecuencia
        self.duracion = duracion
        self.amplitud = amplitud
        self.buffer = self._generar_seno()
        
        # Si se le pasa un objeto Env, lo aplica inmediatamente
        if env:
            self.buffer = env.aplicar(self.buffer, self.duracion)

    def _generar_seno(self) -> np.ndarray:
        total_samples = int(SAMPLE_RATE * self.duracion)
        t = np.linspace(0, self.duracion, total_samples, endpoint=False)
        onda = self.amplitud * np.sin(2 * np.pi * self.frecuencia * t)
        return onda.astype(np.float32)
        
    def __add__(self, otra_onda):
        """Suma (Mix) para acordes, soportando duraciones distintas y Tracks."""
        max_len = max(len(self.buffer), len(otra_onda.buffer))
        # Rellenamos con ceros (silencio) la que sea más corta
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otra_onda.buffer, (0, max_len - len(otra_onda.buffer)))
        
        # SOLUCIÓN: Calculamos la duración real basada en los samples 
        # sin importar si es un Wave o un Track
        nueva_duracion = max_len / SAMPLE_RATE

        nueva_onda = Wave(0, nueva_duracion, 0)
        nueva_onda.buffer = buf1 + buf2
        return nueva_onda

    def __rshift__(self, otro):
        """Sobrecarga del operador >> para iniciar un Track con una Onda."""
        nuevo_track = Track()
        nuevo_track.agregar(self)
        nuevo_track.agregar(otro)
        return nuevo_track

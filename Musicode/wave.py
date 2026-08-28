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
        # Suma (Mix) para acordes
        nueva_onda = Wave(0, self.duracion, 0)
        nueva_onda.buffer = self.buffer + otra_onda.buffer
        return nueva_onda

    def __rshift__(self, otro):
        """Sobrecarga del operador >> para iniciar un Track con una Onda."""
        nuevo_track = Track()
        nuevo_track.agregar(self)
        nuevo_track.agregar(otro)
        return nuevo_track

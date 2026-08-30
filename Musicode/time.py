import numpy as np

from Musicode.engine import SAMPLE_RATE
from Musicode.track import Track


#?EL SILENCIO (Time)
class Time:
    def __init__(self, duracion: float):
        if duracion <0:
            raise ValueError("Error en Time: La duración no puede ser negativa.")
        self.duracion = duracion
        total_samples = int(SAMPLE_RATE * self.duracion)
        # Un silencio no es más que un arreglo de ceros
        self.buffer = np.zeros(total_samples, dtype=np.float32)

    def __rshift__(self, otro):
        """Sobrecarga del operador >> para iniciar un Track con un Silencio."""
        nuevo_track = Track()
        nuevo_track.agregar(self)
        nuevo_track.agregar(otro)
        return nuevo_track

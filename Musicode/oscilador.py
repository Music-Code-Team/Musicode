import numpy as np
import sounddevice as sd

SAMPLE_RATE: int = 44100 

class Wave:
    def __init__(self, frecuencia: float, duracion: float, amplitud: float = 0.5):
        self.frecuencia = frecuencia
        self.duracion = duracion
        self.amplitud = amplitud
        self.buffer = self._generar_seno()

    def _generar_seno(self) -> np.ndarray:
        total_samples = int(SAMPLE_RATE * self.duracion)
        t = np.linspace(0, self.duracion, total_samples, endpoint=False)
        onda = self.amplitud * np.sin(2 * np.pi * self.frecuencia * t)
        return onda.astype(np.float32)

    def reproducir(self):
        sd.play(self.buffer, SAMPLE_RATE)
        sd.wait()

    def __add__(self, otra_onda):
        if len(self.buffer) == len(otra_onda.buffer):
            nueva_onda = Wave(0, self.duracion, 0)
            nueva_onda.buffer = self.buffer + otra_onda.buffer
            return nueva_onda
        else:
            raise ValueError("Las ondas deben tener la misma duración.")
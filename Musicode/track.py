import numpy as np
import sounddevice as sd
from Musicode.eventos import Observador
from Musicode.engine import SAMPLE_RATE
#?LA SECUENCIA (Track)
class Track(Observador):
    def __init__(self):
        # El Track inicia vacío
        super().__init__()
        self.buffer = np.array([], dtype=np.float32)

    def agregar(self, elemento):
        """Añade el buffer de un Wave o un Time al final del Track."""
        self.buffer = np.concatenate([self.buffer, elemento.buffer])

    def __rshift__(self, otro):
        """Permite encadenar (Track >> Wave) o (Track >> Time)."""
        self.agregar(otro)
        return self

    def reproducir(self):
        #!avisa que va a empezar antes de reproducir
        self.emitir("reproduccion_iniciada") 
        sd.play(self.buffer, SAMPLE_RATE)
        sd.wait()
        #!avisa que va a terminar despues de reproducir
        self.emitir("reproduccion_terminada")
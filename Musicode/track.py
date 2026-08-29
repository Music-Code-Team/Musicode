import numpy as np

from Musicode.engine import exportar_wave, reproducir_audio
from Musicode.eventos import Observador


# ?LA SECUENCIA (Track)
class Track(Observador):
    def __init__(self):
        # El Track inicia vacío
        super().__init__()
        self.buffer = np.array([], dtype=np.float32)
    def agregar(self, elemento):
        """Añade el buffer de un Wave o un Time al final del Track."""
        self.buffer = np.concatenate([self.buffer, elemento.buffer])

    def __add__(self, otro_track):
        """Mezcla dos tracks completos para que suenen simultáneamente."""
        nuevo_track = Track()
        
        # Buscamos el tamaño máximo y rellenamos el track más corto con silencios
        max_len = max(len(self.buffer), len(otro_track.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otro_track.buffer, (0, max_len - len(otro_track.buffer)))
        
        nuevo_track.buffer = buf1 + buf2
        return nuevo_track

    def __rshift__(self, otro):
        """Permite encadenar (Track >> Wave) o (Track >> Time)."""
        self.agregar(otro)
        return self

    def reproducir(self,asincrono=True):
        # !avisa que va a empezar antes de reproducir
        cb_inicio = lambda: self.emitir("reproduccion_iniciada")
        cb_fin = lambda: self.emitir("reproduccion_terminada")
        
        return reproducir_audio(
            self.buffer, 
            asincrono=asincrono, 
            callback_inicio=cb_inicio, 
            callback_fin=cb_fin
            )
    def exportar(self, nombre_archivo="mi_pista.wav"):
        """Permite guardar todo el track como un archivo de audio."""
        exportar_wave(self.buffer, nombre_archivo)
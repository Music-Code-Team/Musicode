import numpy as np

from Musicode.engine import exportar_wave, reproducir_audio
from Musicode.eventos import Observador


# ?LA SECUENCIA (Track)
class Track(Observador):
    def __init__(self):
        super().__init__()
        # En lugar de concatenar inmediatamente, guardamos los pedazos
        self._fragmentos = []

    @property
    def buffer(self):
        """Compila la pista de forma 'perezosa' solo cuando se necesita leer."""
        if not self._fragmentos:
            return np.array([], dtype=np.float32)
        
        # Si hay más de un fragmento, los unimos TODOS de un solo golpe
        if len(self._fragmentos) > 1:
            pista_completa = np.concatenate(self._fragmentos)
            # Guardamos el resultado en la lista para no volver a calcularlo
            self._fragmentos = [pista_completa]
            
        return self._fragmentos[0]

    @buffer.setter
    def buffer(self, nuevo_buffer):
        """Permite sobrescribir la pista (necesario para el operador +)."""
        self._fragmentos = [nuevo_buffer]

    def agregar(self, elemento):
        """Añade el buffer a la lista de espera sin hacer copias de memoria pesadas."""
        self._fragmentos.append(elemento.buffer)

    def __add__(self, otro_track):
        """Mezcla dos tracks completos para que suenen simultáneamente."""
        nuevo_track = Track()
        
        # Al llamar a .buffer aquí, los tracks se compilarán automáticamente si tenían notas pendientes
        max_len = max(len(self.buffer), len(otro_track.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otro_track.buffer, (0, max_len - len(otro_track.buffer)))
        
        # Usamos el @buffer.setter que creamos arriba
        suma = buf1 + buf2
        nuevo_track.buffer = np.clip(suma,-1.0,1.0)
        return nuevo_track

    def __rshift__(self, otro):
        """Permite encadenar devolviendo un Track NUEVO (Inmutabilidad estricta)."""
        nuevo_track = Track()
        
        # Copiamos la lista de fragmentos de la pista actual
        nuevo_track._fragmentos = list(self._fragmentos)
        
        # Añadimos el nuevo elemento a la copia
        nuevo_track.agregar(otro)
        
        return nuevo_track

    def reproducir(self, asincrono=True):
        # !avisa que va a empezar antes de reproducir
        cb_inicio = lambda: self.emitir("reproduccion_iniciada")
        cb_fin = lambda: self.emitir("reproduccion_terminada")
        
        # Al llamar a self.buffer, compila todo mágicamente
        return reproducir_audio(
            self.buffer, 
            asincrono=asincrono, 
            callback_inicio=cb_inicio, 
            callback_fin=cb_fin
        )
        
    def exportar(self, nombre_archivo="mi_pista.wav"):
        """Permite guardar todo el track como un archivo de audio."""
        exportar_wave(self.buffer, nombre_archivo)
import numpy as np

from Motor.engine import SAMPLE_RATE, exportar_wave, reproducir_audio
from Motor.eventos import Observador


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

# -- [ MÉTODOS EXPLÍCITOS KODA ] --
    def setEnvelope(self, env):
        """Aplica un ADSR al track completo (después de compilarlo)."""
        duracion_total = len(self.buffer) / SAMPLE_RATE
        # Sobrescribimos el buffer usando el setter mágico
        self.buffer = env.aplicar(self.buffer, duracion_total)
        return self

    def setBPM(self, bpm: float):
        """Configuración de metrónomo."""
        self.bpm = bpm
        print(f"[Track] BPM ajustado a {self.bpm}")
        return self

    def sync(self, modo: str):
        """Define el comportamiento de colisión (stretch/loop)."""
        if modo not in ["stretch", "loop"]:
            raise ValueError("Error: El modo de sync debe ser 'stretch' o 'loop'")
        self.sync_mode = modo
        print(f"[Track] Modo de sincronización ajustado a '{self.sync_mode}'")
        return self

# -- [ MÉTODOS EXPLÍCITOS KODA ] --
    def remove(self, otro):
        """Busca exactamente el patrón de otra pista y lo elimina (Extracción)."""
        b_self = self.buffer
        b_otro = otro.buffer
        
        # Truco de bajo nivel: Buscamos coincidencias exactas en la memoria RAM (bytes)
        str_self = b_self.tobytes()
        str_otro = b_otro.tobytes()
        idx_bytes = str_self.find(str_otro)
        
        if idx_bytes != -1:
            # Sabiendo que los float32 pesan 4 bytes, calculamos el índice real del arreglo
            idx = idx_bytes // 4  
            n = len(b_otro)
            self.buffer = np.concatenate((b_self[:idx], b_self[idx + n:]))
            print("[Track] Patrón encontrado y eliminado con éxito.")
        else:
            print("[Track] No se encontró el patrón acústico en la pista principal.")
        return self

    def export(self, nombre_archivo="mi_pista.wav"):
        """Exporta la pista. (Renombrado para coincidir con la especificación)"""
        exportar_wave(self.buffer, nombre_archivo)

    # -- [ SOBRECARGA DE OPERADORES ] --
    def __sub__(self, otro):
        """Cancelación de Fase para secuencias completas."""
        nuevo_track = Track()
        
        max_len = max(len(self.buffer), len(otro.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otro.buffer, (0, max_len - len(otro.buffer)))
        
        nuevo_track.buffer = np.clip(buf1 - buf2, -1.0, 1.0)
        return nuevo_track

    def __add__(self, otro):
        """Concatena tracks (Secuencia)."""
        nuevo_track = Track()
        nuevo_track._fragmentos = list(self._fragmentos)
        nuevo_track.agregar(otro)
        return nuevo_track

    def __mul__(self, otro):
        """Acordes/Mezcla si es Track/Wave, Volumen si es número."""
        if isinstance(otro, (int, float)):
            nuevo_track = Track()
            buffer_modulado = self.buffer * otro
            nuevo_track.buffer = np.clip(buffer_modulado, -1.0, 1.0)
            return nuevo_track
            
        nuevo_track = Track()
        max_len = max(len(self.buffer), len(otro.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otro.buffer, (0, max_len - len(otro.buffer)))
        nuevo_track.buffer = np.clip(buf1 + buf2, -1.0, 1.0)
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
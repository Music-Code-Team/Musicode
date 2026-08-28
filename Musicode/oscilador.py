import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100

#?ENVOLVENTE ADSR (Env)
class Env:
    def __init__(self, attack_seg: float, decay_seg: float, sustain_vol: float, release_seg: float):
        self.attack = attack_seg
        self.decay = decay_seg
        self.sustain = sustain_vol
        self.release = release_seg

    def aplicar(self, buffer: np.ndarray, duracion_total: float) -> np.ndarray:
        """Modifica la onda original multiplicándola por una curva de volumen."""
        total_samples = len(buffer)
        a_samples = int(self.attack * SAMPLE_RATE)
        d_samples = int(self.decay * SAMPLE_RATE)
        r_samples = int(self.release * SAMPLE_RATE)

        # Generamos un arreglo de volumen 1.0 (sustain por defecto temporal)
        curva = np.ones(total_samples, dtype=np.float32) * self.sustain

        # Attack (Sube de 0 a 1)
        if a_samples > 0:
            curva[:a_samples] = np.linspace(0.0, 1.0, a_samples)
        
        # Decay (Baja de 1 al nivel de Sustain)
        if d_samples > 0 and (a_samples + d_samples) <= total_samples:
            curva[a_samples:a_samples+d_samples] = np.linspace(1.0, self.sustain, d_samples)
        
        # Release (Baja del Sustain a 0)
        if r_samples > 0 and r_samples <= total_samples:
            curva[-r_samples:] = np.linspace(self.sustain, 0.0, r_samples)

        # Multiplicamos el buffer original de la onda por nuestra curva ADSR
        return buffer * curva

#?EL SILENCIO (Time)
class Time:
    def __init__(self, duracion: float):
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

#?LA SECUENCIA (Track)
class Track:
    def __init__(self):
        # El Track inicia vacío
        self.buffer = np.array([], dtype=np.float32)

    def agregar(self, elemento):
        """Añade el buffer de un Wave o un Time al final del Track."""
        self.buffer = np.concatenate([self.buffer, elemento.buffer])

    def __rshift__(self, otro):
        """Permite encadenar (Track >> Wave) o (Track >> Time)."""
        self.agregar(otro)
        return self

    def reproducir(self):
        sd.play(self.buffer, SAMPLE_RATE)
        sd.wait()
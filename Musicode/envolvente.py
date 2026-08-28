import numpy as np
import sounddevice as sd
from Musicode.engine import SAMPLE_RATE
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


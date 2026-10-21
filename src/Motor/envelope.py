import numpy as np

from Motor.engine import SAMPLE_RATE


# =========================================================
# TICKET #15: ENVELOPE CLASS
# =========================================================
class Envelope:
    """
    Envolvente ADSR (Attack, Decay, Sustain, Release).
    Esculpe la amplitud (volumen) del sonido a lo largo de su vida útil para naturalizarlo.
    """
    def __init__(self, attack_seg: float, decay_seg: float, sustain_vol: float, release_seg: float):
        # Validaciones semánticas estrictas
        if any(v < 0 for v in [attack_seg, decay_seg, release_seg]):
            raise ValueError("Error Semántico: Los tiempos ADSR no pueden ser negativos.")
        if not (0.0 <= sustain_vol <= 1.0):
            raise ValueError("Error Semántico: El sustain debe estar entre 0.0 y 1.0.")
            
        self.attack = attack_seg
        self.decay = decay_seg
        self.sustain = sustain_vol
        self.release = release_seg

    def aplicar(self, buffer: np.ndarray, duracion_total: float) -> np.ndarray:
        """
        Modifica la onda original multiplicándola por la curva de volumen ADSR.
        """
        total_samples = len(buffer)
        a_samples = int(self.attack * SAMPLE_RATE)
        d_samples = int(self.decay * SAMPLE_RATE)
        r_samples = int(self.release * SAMPLE_RATE)

        # Evitamos desbordamientos si los tiempos son más largos que la nota misma
        a_samples = min(a_samples, total_samples)
        d_samples = min(d_samples, total_samples - a_samples)
        r_samples = min(r_samples, total_samples - a_samples - d_samples)

        # Generamos un arreglo de volumen constante en el nivel de Sustain
        curva = np.ones(total_samples, dtype=np.float32) * self.sustain

        # Attack (Sube de 0 a 1)
        if a_samples > 0:
            curva[:a_samples] = np.linspace(0.0, 1.0, a_samples)
        
        # Decay (Baja de 1 al nivel de Sustain)
        if d_samples > 0:
            curva[a_samples:a_samples+d_samples] = np.linspace(1.0, self.sustain, d_samples)
        
        # Release (Baja del Sustain a 0 desde el final)
        if r_samples > 0:
            curva[-r_samples:] = np.linspace(self.sustain, 0.0, r_samples)

        return buffer * curva
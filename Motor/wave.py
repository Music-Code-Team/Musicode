import numpy as np

from Motor.engine import SAMPLE_RATE
from Motor.envelope import Envelope
from Motor.track import Track


class Wave:
    def __init__(self, frecuencia: float = 0.0, duracion: float = 0.0, amplitud: float =  0.5, tipo: str = "sin", env: Envelope = None, buffer: np.ndarray = None):
        self.frecuencia = frecuencia
        self.duracion = duracion
        self.amplitud = amplitud
        print("tipo")
        print(tipo)
        self.tipo = tipo.lower()
        
        # Si la onda ya viene pre-calculada matemáticamente (ej. por sumar acordes)
        if buffer is not None:
            self.buffer = buffer
        else:
            # 1. VALIDACIONES ESTRICTAS para creación nueva
            if frecuencia <= 0:
                raise ValueError("Error en Wave: La frecuencia debe ser mayor a 0 Hz.")
            if duracion < 0:
                raise ValueError("Error en Wave: La duración no puede ser negativa.")
            if amplitud < 0:
                raise ValueError("Error en Wave: La amplitud no puede ser negativa.")

            # 2. GENERACIÓN CONDICIONAL (El motor monolítico)
            self.buffer = self._generar_forma_onda()
        
        # Aplicamos la envolvente si existe
        if env:
            self.buffer = env.aplicar(self.buffer, self.duracion)

    def _generar_forma_onda(self) -> np.ndarray:
        """Genera la onda basándose en el parámetro de texto 'tipo'."""
        total_samples = int(SAMPLE_RATE * self.duracion)
        t = np.linspace(0, self.duracion, total_samples, endpoint=False)
        
        # Evaluamos qué sintetizador pidió el usuario
        if self.tipo == "sin":
            onda = self.amplitud * np.sin(2 * np.pi * self.frecuencia * t)
            
        elif self.tipo == "square":
            seno = np.sin(2 * np.pi * self.frecuencia * t)
            onda = self.amplitud * np.where(seno >= 0, 1.0, -1.0)
            
        elif self.tipo == "saw":
            onda = self.amplitud * (2.0 * ((t * self.frecuencia) % 1.0) - 1.0)
            
        else:
            raise ValueError(f"Error en Wave: El tipo '{self.tipo}' no está soportado. Usa 'sin', 'square' o 'saw'.")
            
        return onda.astype(np.float32)

# -- [ MÉTODOS EXPLÍCITOS KODA ] --
    def setEnvelope(self, env: Envelope):
        """Esculpe el volumen de la onda a lo largo del tiempo."""
        self.buffer = env.aplicar(self.buffer, self.duracion)
        return self # Permite encadenamiento

    def reverse(self):
        """Invierte el arreglo para que suene al revés."""
        self.buffer = self.buffer[::-1]
        return self

    def cut(self, tiempo_seg: float):
        """Recorta el final de la onda."""
        recorte_samples = int(tiempo_seg * SAMPLE_RATE)
        if recorte_samples < len(self.buffer):
            self.buffer = self.buffer[:-recorte_samples]
            self.duracion -= tiempo_seg
        return self

    def setFrequency(self, freq: float):
        """Modifica el tono y regenera la onda base."""
        if freq <= 0:
            raise ValueError("Error Semántico: La frecuencia debe ser mayor a 0.")
        self.frecuencia = freq
        self.buffer = self._generar_forma_onda()
        return self

    def addFrequency(self, freq: float):
        return self.setFrequency(self.frecuencia + freq)

    def subFrequency(self, freq: float):
        return self.setFrequency(self.frecuencia - freq)

    def setDuration(self, tiempo_seg: float, modo: str = "stretch"):
        """Sobrescribe la duración (estira o recorta la onda a un tiempo exacto)."""
        if tiempo_seg < self.duracion:
            return self.cut(self.duracion - tiempo_seg)
            
        target_samples = int(tiempo_seg * SAMPLE_RATE)
        if modo == "loop":
            reps = int(np.ceil(target_samples / len(self.buffer)))
            self.buffer = np.tile(self.buffer, reps)[:target_samples]
        else: # Stretch (Interpolación Lineal básica)
            indices = np.linspace(0, len(self.buffer) - 1, target_samples)
            self.buffer = np.interp(indices, np.arange(len(self.buffer)), self.buffer).astype(np.float32)
            
        self.duracion = tiempo_seg
        return self

    def addDuration(self, tiempo_seg: float, at: float | None = None):
        """Le suma silencio en una marca de tiempo específica (o al final)."""
        silencio = np.zeros(int(tiempo_seg * SAMPLE_RATE), dtype=np.float32)
        if at is None:
            self.buffer = np.concatenate((self.buffer, silencio))
        else:
            split_idx = int(at * SAMPLE_RATE)
            self.buffer = np.concatenate((self.buffer[:split_idx], silencio, self.buffer[split_idx:]))
        self.duracion += tiempo_seg
        return self

    def remove(self, tiempo_seg: float):
        """Remueve la cantidad de segundos indicada desde el INICIO de la onda."""
        remove_samples = int(tiempo_seg * SAMPLE_RATE)
        if remove_samples < len(self.buffer):
            self.buffer = self.buffer[remove_samples:]
            self.duracion -= tiempo_seg
        else:
            self.buffer = np.array([], dtype=np.float32)
            self.duracion = 0.0
        return self

    # -- [ SOBRECARGA DE OPERADORES ] --
    def __sub__(self, otro):
        """Cancelación de Fase Acústica (Resta de frecuencias)."""
        max_len = max(len(self.buffer), len(otro.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otro.buffer, (0, max_len - len(otro.buffer)))
        
        nueva_duracion = max_len / SAMPLE_RATE
        resta_segura = np.clip(buf1 - buf2, -1.0, 1.0)
        return Wave(duracion=nueva_duracion, tipo="mixed", buffer=resta_segura)
    
    def __add__(self, otra_onda):
        """Concatena (Secuencia) creando un nuevo Track."""
        nuevo_track = Track()
        nuevo_track.agregar(self)
        nuevo_track.agregar(otra_onda)
        return nuevo_track

    def __mul__(self, otro):
        """Polifonía/Acorde si es otra onda, o Modulación si es un número."""
        if isinstance(otro, (int, float)):
            # Modulación de volumen (por ahora)
            buffer_modulado = self.buffer * otro
            return Wave(duracion=self.duracion, tipo="mixed", buffer=np.clip(buffer_modulado, -1.0, 1.0))
            
        # Mezcla de audios (Polifonía)
        max_len = max(len(self.buffer), len(otro.buffer))
        buf1 = np.pad(self.buffer, (0, max_len - len(self.buffer)))
        buf2 = np.pad(otro.buffer, (0, max_len - len(otro.buffer)))
        
        nueva_duracion = max_len / SAMPLE_RATE
        suma_segura = np.clip(buf1 + buf2, -1.0, 1.0)
        return Wave(duracion=nueva_duracion, tipo="mixed", buffer=suma_segura)
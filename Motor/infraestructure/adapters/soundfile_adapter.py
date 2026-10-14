import os

import soundfile as sf

from Motor.application.interfaces.audio_decoder import IAudioDecoder
from Motor.domain.entities.wave import Wave


class SoundfileDecoderAdapter(IAudioDecoder):
    def decode_file(self, file_path: str) -> Wave:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: El archivo '{file_path}' no existe.")
            
        print(f"[Motor] Decodificando media: {file_path}...")
        buffer, original_sr = sf.read(file_path, dtype='float32')
        
        if len(buffer.shape) > 1:
            buffer = buffer.mean(axis=1)
            
        duracion_real = len(buffer) / original_sr
        
        return Wave(frecuencia=0.0, duracion=duracion_real, tipo="sample", buffer=buffer)
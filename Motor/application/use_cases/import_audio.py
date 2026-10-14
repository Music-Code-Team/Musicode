from Motor.application.interfaces.audio_decoder import IAudioDecoder
from Motor.application.interfaces.wave_repository import IWaveRepository


class ImportAudioUseCase:
    def __init__(self, decoder: IAudioDecoder, repository: IWaveRepository):
        self.decoder = decoder
        self.repository = repository

    def execute(self, file_path: str, variable_name: str):
        # 1. Usar la infraestructura (el adaptador) para leer el disco duro
        nueva_onda = self.decoder.decode_file(file_path)
        
        # 2. Asignarle un ID (el nombre de la variable en Koda)
        nueva_onda.id = variable_name
        
        # 3. Guardar la entidad pura en la memoria RAM (el repositorio)
        self.repository.save(nueva_onda)
        
        return nueva_onda
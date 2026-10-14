import json
import os

from Motor.application.interfaces.wave_repository import IWaveRepository
from Motor.domain.entities.wave import Wave


class JsonWaveRepository(IWaveRepository):
    """
    Adaptador de Infraestructura: Persiste las ondas en un archivo JSON local
    en lugar de la memoria RAM.
    """
    def __init__(self, file_path: str = "ondas_musicode.json"):
        self.file_path = file_path
        # Si el archivo no existe, lo crea vacío
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def get(self, wave_id: str) -> Wave:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if wave_id in data:
            item = data[wave_id]
            return Wave(
                # En un entorno real se recuperarían todos los atributos necesarios
                frecuencia=item["frecuencia"],
                duracion=item["duracion"],
                amplitud=item["amplitud"],
                tipo=item["tipo"]
            )
        return None

    def save(self, wave: Wave) -> None:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Almacenamos los atributos principales de la entidad (Simulando persistencia)
        data[wave.frecuencia] = { # Idealmente se usaría wave.id, pero usamos frecuencia por simplificar el ejemplo
            "frecuencia": wave.frecuencia,
            "duracion": wave.duracion,
            "amplitud": wave.amplitud,
            "tipo": wave.tipo
        }
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
from Motor.application.interfaces.wave_repository import IWaveRepository


class AlterWaveFrequencyUseCase:
    def __init__(self, repository: IWaveRepository):
        self.repository = repository

    def execute(self, wave_id: str, hz_to_subtract: float) -> float:
        wave = self.repository.get(wave_id)
        if not wave:
            raise ValueError("Onda no encontrada")
        
        wave.sub_frequency(hz_to_subtract)
        self.repository.save(wave)
        return wave.frequency
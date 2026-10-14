from Motor.application.interfaces.wave_repository import IWaveRepository
from Motor.domain.entities.wave import Wave


class InMemoryWaveRepository(IWaveRepository):
    def __init__(self):
        self._storage = {}

    def get(self, wave_id: str) -> Wave:
        return self._storage.get(wave_id)

    def save(self, wave: Wave) -> None:
        self._storage[wave.id] = wave
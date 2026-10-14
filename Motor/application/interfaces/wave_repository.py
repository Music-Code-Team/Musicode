from abc import ABC, abstractmethod

from Motor.domain.entities.wave import Wave


class IWaveRepository(ABC):
    @abstractmethod
    def get(self, wave_id: str) -> Wave:
        pass

    @abstractmethod
    def save(self, wave: Wave) -> None:
        pass
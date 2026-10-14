from abc import ABC, abstractmethod

from Motor.domain.entities.wave import Wave


class IAudioDecoder(ABC):
    @abstractmethod
    def decode_file(self, file_path: str) -> Wave:
        """Contrato: Recibe una ruta y debe devolver un objeto Wave puro."""

        pass  # noqa: PIE790 
    # !Solo ignoramos la warning nada de que preocuparse

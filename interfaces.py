from abc import ABC, abstractmethod
from typing import List

class FilenameExporter(ABC):
    @abstractmethod
    def export_filenames(self, album_name: str, output_path: str) -> None:
        pass

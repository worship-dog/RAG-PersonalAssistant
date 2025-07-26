
from abc import ABC, abstractmethod
import os


class FileReader(ABC):
    @abstractmethod
    def read(self, file_path):
        pass

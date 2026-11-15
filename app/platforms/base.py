
from abc import ABC, abstractmethod


class BasePlatform(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    async def post(self, message: str) -> dict:
        pass

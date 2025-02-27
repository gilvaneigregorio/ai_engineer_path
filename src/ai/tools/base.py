from abc import ABC, abstractmethod


class BaseTool(ABC):
    @abstractmethod
    def get_function_definition(self) -> dict:
        pass

    @abstractmethod
    def call(self, *args, **kwargs) -> str:
        pass

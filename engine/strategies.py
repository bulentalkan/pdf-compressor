from abc import ABC, abstractmethod
from .options import CompressionOptions

class CompressionStrategy(ABC):
    @abstractmethod
    def get_options(self) -> CompressionOptions:
        ...     #  ellipsis (...) is used to indicate that the method is abstract and should be implemented by subclasses
        
class FastStrategy(CompressionStrategy):
    def get_options(self) -> CompressionOptions:
        return CompressionOptions(gs_preset="printer") 


class BalancedStrategy(CompressionStrategy):
    def get_options(self) -> CompressionOptions:
        return CompressionOptions(gs_preset="ebook")


class MaxCompressionStrategy(CompressionStrategy):
    def get_options(self) -> CompressionOptions:
        return CompressionOptions(gs_preset="screen")


if __name__ == "__main__":
    for strategy in [FastStrategy(), BalancedStrategy(), MaxCompressionStrategy()]:
        print(strategy.get_options())
from pathlib import Path
from .document import PDFDocument
from .engine import PDFCompressor
from .strategies import CompressionStrategy, BalancedStrategy
from .result import CompressionResult
from .exceptions import PDFCompressionError

class BatchCompressor:


    def __init__(self, compressor: PDFCompressor | None = None) -> None:
            self.compressor = compressor or PDFCompressor()
    
    
    
    
    def compress_all(self, paths: list[Path], strategy: CompressionStrategy) -> list[CompressionResult]: 
          results = []
    
          for path in paths:
                 try:
                        doc = PDFDocument(path)
                        result = self.compressor.compress(doc, strategy)
                        results.append(result)
                 except PDFCompressionError as e:
                        print(f"Dosya {path} sıkıştırılamadı: {e}")
          return results






if __name__ == "__main__":
       dosyalar = [Path("test.pdf"), Path("olmayan.pdf")]   
       strategy = BalancedStrategy()
       batch = BatchCompressor()
       sonuclar = batch.compress_all(dosyalar, strategy)
       print("Sıkıştırma sonuçları:" , sonuclar)
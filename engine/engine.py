from pydoc import doc

from ghostscript_runner import GhostscriptRunner
from pathlib import Path
import time
from document import PDFDocument
from strategies import CompressionStrategy, BalancedStrategy
from result import CompressionResult
from options import CompressionOptions

class PDFCompressor:
    def __init__(self, runner: GhostscriptRunner | None = None) -> None:
        # if runner is None create a default GhostscriptRunner instance
        # eğer runner verilmezse kendi GhostscriptRunner()'ını oluştur
        self.runner = runner or GhostscriptRunner()

    def compress(self,document: PDFDocument, strategy: CompressionStrategy, output_dir: Path | None = None) -> CompressionResult:
        document.validate()  # validate the document before compression-sıkıştırmadan önce pdf dosyasını doğrulama kısmı
        options = strategy.get_options()  # get the options from the strategy-stratejiden sıkıştırma seçeneklerini al
        yeni_dosya_adi = document.path.stem + options.output_suffix + document.path.suffix
        klasor = output_dir or document.path.parent
        output_path = klasor / yeni_dosya_adi
        baslangic = time.perf_counter()
        self.runner.run(document.path, output_path, options)
        bitis = time.perf_counter()
        sure = bitis - baslangic
        compressed_size = output_path.stat().st_size
        return CompressionResult(original_size= document.original_size_bytes, compressed_size= compressed_size, output_path=output_path, duration_seconds=sure)

    if __name__ == "__main__":
        strategy = BalancedStrategy()
        compressor = PDFCompressor()
        compressed_result = compressor.compress(doc, strategy)
        print(f"Sıkıştırma tamamlandı: {compressed_result}")


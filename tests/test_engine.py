from pathlib import Path
from engine.engine import PDFCompressor
from engine.document import PDFDocument
from engine.strategies import BalancedStrategy
from engine.exceptions import CorruptPDFError
import pytest

def test_compress_raises_on_missing_file():
    compressor = PDFCompressor()
    doc = PDFDocument(Path("olmayan.pdf"))
    strategy = BalancedStrategy()
    with pytest.raises(CorruptPDFError):
        compressor.compress(doc, strategy)
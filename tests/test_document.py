import pytest
from engine.exceptions import CorruptPDFError
from engine.document import PDFDocument
from pathlib import Path 



def test_valid_pdf_passes_validation():
    yol = Path("tests/fixtures/sample.pdf")
    doc = PDFDocument(yol)
    doc.validate()
    assert doc.page_count > 0



def test_missing_pdf_raises_corrupt_error():
    yol = Path("tests/fixtures/olmayan.pdf")
    doc = PDFDocument(yol)
    with pytest.raises(CorruptPDFError):
        doc.validate()
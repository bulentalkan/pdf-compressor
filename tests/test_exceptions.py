from engine.exceptions import PDFCompressionError ,CorruptPDFError
import pytest

def test_corrupt_pdf_error_is_pdf_compression_error():
    assert issubclass(CorruptPDFError,  PDFCompressionError)


def test_raising_corrupt_pdf_error():
    with pytest.raises(CorruptPDFError):
        raise CorruptPDFError("test mesajı")
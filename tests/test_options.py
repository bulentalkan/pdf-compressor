import pytest 
from engine.options import CompressionOptions

def test_valid_preset_creates_options():
    options = CompressionOptions(gs_preset="ebook")
    assert options.gs_preset == "ebook"


def test_invalid_preset_raises_value_error():
    with pytest.raises(ValueError):
        CompressionOptions(gs_preset="Geçersiz Seçenek")
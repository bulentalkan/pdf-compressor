from pathlib import Path
from engine.result import CompressionResult


def test_reduction_percent():
    result = CompressionResult(
        original_size = 5000000,
        compressed_size = 2000000,
        output_path = Path("output.pdf"),
        duration_seconds = 2.5      
    )

    assert result.reduction_percent == 60.0



def test_str_format():
    result = CompressionResult(
        original_size=5000000,
        compressed_size=2000000,
        output_path=Path("output.pdf"),
        duration_seconds=2.5
    )
    assert str(result) == "4.8 MB -> 1.9 MB (%60 azaldı, 2.5 sn)"
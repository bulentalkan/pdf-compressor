from pathlib import Path
from engine.batch import BatchCompressor

def test_compress_all_skips_invalid_files():
    batch = BatchCompressor()
    sonuclar = batch.compress_all([Path("olmayan1.pdf"), Path("olmayan2.pdf")], None)
    assert sonuclar == []
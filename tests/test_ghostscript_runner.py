import pytest
from engine.ghostscript_runner import GhostscriptRunner
from engine.options import CompressionOptions
from pathlib import Path


def test_is_available_bool():
    sonuc = GhostscriptRunner.is_available()
    assert isinstance(sonuc, bool)



def test_build_command():
    runner = GhostscriptRunner()
    options = CompressionOptions(gs_preset = "ebook")
    komut =  runner.build_command(Path("test.pdf"), Path("output.pdf"), options)
    assert "-dPDFSETTINGS=/ebook" in komut

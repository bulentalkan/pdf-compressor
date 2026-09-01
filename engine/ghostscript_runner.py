import shutil
import subprocess
from    exceptions import GhostscriptNotFoundError, PDFCompressionError
from options import CompressionOptions 
from pathlib import Path

class GhostscriptRunner:
    @staticmethod
    
    def is_available() -> bool:
        gs_yolu = shutil.which("gs") or shutil.which("gswin64c")
        if gs_yolu is not None:
            return True
        else: 
            return False
    # in here, we check if the ghostscript executable is available in the system's path. if it returns a path it means gs is available, otherwise, it's not
    # burada yaptığımız şey, aradığımız ghostscript dosyasının sistemde olup olmadığını kontrol etmek. eğer bir şey return ediyorsa var, etmiyorsa yok.

    def build_command(self, input_path: Path, output_path: Path, options:CompressionOptions) -> list[str]:
            return [
                 "gs", 
                 "-sDEVICE=pdfwrite", f"-dPDFSETTINGS=/{options.gs_preset}","-dNOPAUSE",
                 "-dBATCH", f"-sOutputFile={output_path}", 
                 str(input_path)
             ]

    def run(self, input_path: Path, output_path: Path, options: CompressionOptions) -> None:
        if not self.is_available():
            raise GhostscriptNotFoundError("Ghostscript sistemde bulunamadı.")

        command = self.build_command(input_path, output_path, options)
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise PDFCompressionError(f"Ghostscript hata verdi: {result.stderr}")



if __name__ == "__main__":
    print(GhostscriptRunner.is_available())
    object = GhostscriptRunner()
    print(object.build_command(Path("test.pdf"), Path("cikti.pdf"), CompressionOptions(gs_preset="ebook")))
    object.run(Path("test.pdf"), Path("cikti.pdf"), CompressionOptions(gs_preset="ebook")) 
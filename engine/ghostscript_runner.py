import shutil
import subprocess
import sys
from pathlib import Path

from .exceptions import GhostscriptNotFoundError, PDFCompressionError
from .options import CompressionOptions


class GhostscriptRunner:
    @staticmethod
    def _vendor_gs_path() -> Path:
        # Bundling (PyInstaller) sonrası, gswin64c.exe artık proje kökünün yanında değil,
        # onefile .exe'nin çalışma anında kendini açtığı geçici klasörde (sys._MEIPASS) olacak.
        # Kaynaktan çalışırken (frozen değilken) proje kökü, bu dosyanın iki üst klasörü
        # (engine/ghostscript_runner.py -> engine/ -> proje kökü).
        if getattr(sys, "frozen", False):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent
        return base_dir / "vendor" / "gs" / "bin" / "gswin64c.exe"

    @staticmethod
    def _resolve_ghostscript_path() -> str | None:
        # Tek doğru kaynak (single source of truth): önce bundled/vendored kopyaya bak,
        # yoksa sistemin PATH'ine düş. is_available() ve build_command() artık ikisi de
        # bu metodu çağırıyor, yani "bulunan yol" ile "gerçekten kullanılan yol" hep
        # aynı oluyor - eski haliyle build_command()'ın "gs"'i hardcode etmesinden
        # kaynaklanan tutarsızlık (bkz. notes.md, J bölümü) buradan çözülüyor.
        vendor_path = GhostscriptRunner._vendor_gs_path()
        if vendor_path.exists():
            return str(vendor_path)
        return shutil.which("gswin64c") or shutil.which("gs")

    @staticmethod
    def is_available() -> bool:
        return GhostscriptRunner._resolve_ghostscript_path() is not None

    def build_command(self, input_path: Path, output_path: Path, options: CompressionOptions) -> list[str]:
        gs_yolu = self._resolve_ghostscript_path()
        return [
            gs_yolu,
            "-sDEVICE=pdfwrite", f"-dPDFSETTINGS=/{options.gs_preset}", "-dNOPAUSE",
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

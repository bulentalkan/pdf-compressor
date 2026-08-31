from pathlib import Path
from exceptions import CorruptPDFError, UnsupportedPDFError
import pikepdf


class PDFDocument:
    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    def original_size_bytes(self) -> int:
        return self.path.stat().st_size

    @property
    def page_count(self) -> int:
        with pikepdf.open(self.path) as pdf:
            return len(pdf.pages)  
    # pikepdf/PyMuPDF gibi kütüphanelerle pdfleri aç,oku,kapat - sadece ve sadece bilgi için 

    def validate(self) -> None:
        if not self.path.exists():
            raise CorruptPDFError(f"{self.path} dosyası bulunamadı.")

        try:
            with pikepdf.open(self.path) as pdf:
                pass
        except pikepdf.PasswordError:
            raise UnsupportedPDFError(f"{self.path} şifre korumalı.")

        except pikepdf.PdfError:
            raise CorruptPDFError(f"{self.path} bozuk veya desteklenmeyen bir pdf formatı.")

        # dosya yoksa/açılamıyorsa (yani bozuksa falan) CorruptPDFError 
        # dosya şifreli bir şeyse veya format desteklenmiyorsa UnsupportedPDFError
 

if __name__ == "__main__":
    doc = PDFDocument(Path(r"C:\Users\mikro\OneDrive\Desktop\2122 mufredat.pdf"))
    doc.validate()
    print("Dosya geçerli bir pdf dosyasıdır.")
    print(f"Dosya boyutu: {doc.original_size_bytes} bytes") 
    print(f"Sayfa sayısı: {doc.page_count}")
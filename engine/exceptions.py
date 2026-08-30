class PDFCompressionError(Exception):
    """raises when there is an error during pdf compression"""
    pass

class CorruptPDFError(PDFCompressionError):
    """raises when the pdf is corrupt
     if the file looks like a pdf but is not a valid pdf """
   
    pass

class UnsupportedPDFError(PDFCompressionError):
    """raises when the pdf is not supported"""
    pass  

class GhostscriptNotFoundError(PDFCompressionError):
    """raises when the ghostscript is not found"""
    pass

if __name__ == "__main__":
    try:
        raise CorruptPDFError("yarrak")
    except PDFCompressionError as e:
        print(f"yakalandı: {e}")
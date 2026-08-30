from dataclasses import dataclass

@dataclass
class CompressionOptions:
    gs_preset : str
    strip_metadata : bool = True
    output_suffix : str = "_compressed"
    ALLOWED_PRESETS  = ["screen", "ebook", "printer", "prepress"]
    def __post_init__(self):
        """is gs_preset a valid preset? if not, raise ValueError"""

        if self.gs_preset not in self.ALLOWED_PRESETS:
            raise ValueError(f"Invalid gs_preset: {self.gs_preset}.")

if __name__ == "__main__":
    a = CompressionOptions(gs_preset="ebook")
    b = CompressionOptions(gs_preset="screen")
    print(a.ALLOWED_PRESETS is b.ALLOWED_PRESETS)
    # ALLOWED_PRESETS nesneler arasında paylaşılıyor mu diye küçük bir test
    # paylaşılıyor çünkü bu bir class variable instance variable değil. nesneye bağlı değil, classa bağlı. 
        
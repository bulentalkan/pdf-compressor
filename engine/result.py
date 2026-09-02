from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompressionResult:
    original_size: int
    compressed_size: int
    output_path: Path
    duration_seconds: float

    @property
    def reduction_percent(self):
        return   (self.original_size - self.compressed_size) / self.original_size * 100 

    def __str__(self) -> str:
        orijinal_mb = self.original_size / (1024 * 1024)
        sikistirilmis_mb = self.compressed_size / (1024 * 1024)
        return f"{orijinal_mb:.1f} MB -> {sikistirilmis_mb:.1f} MB (%{self.reduction_percent:.0f} azaldı, {self.duration_seconds:.1f} sn)"



if __name__ == "__main__":
    result = CompressionResult(original_size=5000000, compressed_size=2000000, output_path=Path("output.pdf"), duration_seconds=2.5)
    print(result)
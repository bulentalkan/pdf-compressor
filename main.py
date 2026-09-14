import argparse
from pathlib import Path
from engine.batch import BatchCompressor
from engine.exceptions import CorruptPDFError
from engine.strategies import FastStrategy, BalancedStrategy, MaxCompressionStrategy


parser = argparse.ArgumentParser()

parser.add_argument("files", nargs = "+", help="Sıkıştırılacak PDF dosyaları")
# nargs -> en az bir, istersen daha fazla değer kabul et anlamına geliyor
# nargs -> at least one, can accept more values if you want

parser.add_argument("--strategy", choices=["fast", "balanced", "max"], default="balanced", help="Sıkıştırma Seçeneği")

args = parser.parse_args()


stratejiler = {
    "fast": FastStrategy(),
    "balanced": BalancedStrategy(),
    "max": MaxCompressionStrategy(),
}
secilen_strateji = stratejiler[args.strategy]


dosya_yollari = [Path(dosya) for dosya in args.files]



batch = BatchCompressor()
sonuclar = batch.compress_all(dosya_yollari, secilen_strateji)


for sonuc in sonuclar:
    print(sonuc)
# pdf-compressor

A tool that compresses pdf files locally using Ghostscript. No file ever leaves your machine.

## WHY

Most online pdf compressors require uploading your files to a third party server. For documents containing personal or client data (the kind lawyers, hr managers etc. handle daily), that's unacceptable under privacy regulations like KVKK(Kişisel Verilerin Korunması Kanunu -> basically Türkiye's GDPR). This tool does the same job offline. Your pdf stays on your computer from start to finish.

It's also a personal training project of mine to develop my programming skills.


## How It Works 

So basically what it does is, it calls Ghostscript with `subprocess`.
It does not compress the pdf on its own. 
It also uses `pikepdf`, but only to validate the file and read the metadata.


## Requirements

### Using the pre-built Windows executable (`PDFCompressor.exe`)

- Nothing else. Ghostscript is bundled inside the `.exe` — no separate installation needed.

### Running from source

- Python 3.10+
- [Ghostscript](https://www.ghostscript.com/releases/gsdnld.html) — must be installed separately and available on your system PATH. This tool calls it as an external program.
- Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Installation 

### Option A — Windows executable (recommended for non-technical users)

Just run `PDFCompressor.exe`. Ghostscript is bundled inside, so there's nothing else to install.

> **Note:** Windows may show a SmartScreen warning ("Windows protected your PC") the first time you run it, because the `.exe` isn't code-signed. This is a reputation/signing warning, not a virus detection — click "More info" → "Run anyway" to proceed.

The bundled Ghostscript is licensed under AGPL-3.0 — see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for details.

### Option B — Run from source

1) Clone the repo:

```bash 
git clone https://github.com/bulentalkan/pdf-compressor.git
cd pdf-compressor
```

2) Install the required Python packages:

```bash
pip install -r requirements.txt
``` 
3) Install Ghostscript separately (requirements above) and make sure that it's available on your PATH.


## Usage

### GUI

```bash
python gui.py
```

A simple desktop interface (English/Turkish) — select one or more PDFs, pick a strategy, and compress. This is also what `PDFCompressor.exe` runs.

### Command line

Compress a file with the default strategy (the balanced one):
```bash
python main.py document.pdf
```

Compress multiple files at once:

```bash
python main.py file1.pdf file2.pdf file3.pdf
```

Choose a compression strategy:

```bash
python main.py document.pdf --strategy fast
```

Available ones:

- `fast` — quick compression, minimal quality loss
- `balanced` — good trade-off between size and quality (default)
- `max` — smallest file size, most aggressive compression

## Project Structure

```
pdf-compressor/
├── main.py                    # CLI entry point
├── gui.py                     # desktop GUI (customtkinter, EN/TR)
├── requirements.txt
├── conftest.py                # lets pytest find the engine/ package
├── THIRD_PARTY_LICENSES.md    # license notice for bundled Ghostscript (AGPL-3.0)
├── vendor/gs/                 # bundled Ghostscript binaries (not committed — see .gitignore)
├── engine/
│   ├── __init__.py
│   ├── document.py            # PDFDocument — validation, metadata
│   ├── options.py             # CompressionOptions — Ghostscript preset settings
│   ├── strategies.py          # Fast/Balanced/Max strategies
│   ├── ghostscript_runner.py  # builds and runs the Ghostscript command
│   ├── engine.py              # PDFCompressor — orchestrates a single compression
│   ├── batch.py               # BatchCompressor — compresses multiple files
│   ├── result.py              # CompressionResult — before/after stats
│   └── exceptions.py          # custom exception hierarchy
└── tests/                     # pytest test suite (one file per module)
    └── fixtures/               # sample PDF used by tests
```


## License

MIT — see [LICENSE](LICENSE) for details. Note: the bundled Windows executable also includes Ghostscript, which is licensed separately under AGPL-3.0 — see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

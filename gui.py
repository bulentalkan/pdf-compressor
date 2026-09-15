import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path

from engine.batch import BatchCompressor
from engine.strategies import FastStrategy, BalancedStrategy, MaxCompressionStrategy
from engine.exceptions import GhostscriptNotFoundError

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

STRATEGY_OBJECTS = {
    "fast": FastStrategy(),
    "balanced": BalancedStrategy(),
    "max": MaxCompressionStrategy(),
}

TEXT = {
    "English": {
        "window_title": "PDF Compressor",
        "title": "PDF Compressor",
        "select_files": "Select PDF Files",
        "no_files": "No files selected",
        "strategy_label": "Strategy",
        "compress": "Compress",
        "compressing": "Compressing...",
        "done": "Done.",
        "results": "Results",
        "no_files_title": "No files",
        "no_files_message": "Please select at least one PDF file first.",
        "no_results": "No files were compressed. Check that the selected files are valid PDFs.",
        "gs_not_found": "Ghostscript is not installed or not found on your PATH.",
        "error_title": "Error",
        "strategies": {"fast": "Fast", "balanced": "Balanced", "max": "Max Compression"},
    },
    "Türkçe": {
        "window_title": "PDF Sıkıştırıcı",
        "title": "PDF Sıkıştırıcı",
        "select_files": "PDF Dosyaları Seç",
        "no_files": "Dosya seçilmedi",
        "strategy_label": "Strateji",
        "compress": "Sıkıştır",
        "compressing": "Sıkıştırılıyor...",
        "done": "Tamamlandı.",
        "results": "Sonuçlar",
        "no_files_title": "Dosya yok",
        "no_files_message": "Lütfen önce en az bir PDF dosyası seçin.",
        "no_results": "Hiçbir dosya sıkıştırılamadı. Seçilen dosyaların geçerli PDF olduğundan emin olun.",
        "gs_not_found": "Ghostscript kurulu değil ya da PATH'te bulunamadı.",
        "error_title": "Hata",
        "strategies": {"fast": "Hızlı", "balanced": "Dengeli", "max": "Maksimum Sıkıştırma"},
    },
}


class PDFCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language = "English"
        self.selected_strategy_key = "balanced"
        self.selected_files = []
        self.batch = BatchCompressor()

        self.geometry("420x580")
        self.minsize(420, 580)

        self._build_widgets()
        self._apply_language()

    def _build_widgets(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=24)

        top_row = ctk.CTkFrame(container, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 16))
        self.title_label = ctk.CTkLabel(top_row, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(side="left")
        self.language_menu = ctk.CTkOptionMenu(
            top_row, values=list(TEXT.keys()), width=110, command=self.change_language
        )
        self.language_menu.set(self.language)
        self.language_menu.pack(side="right")

        self.select_button = ctk.CTkButton(container, text="", command=self.select_files, height=36)
        self.select_button.pack(fill="x", pady=(0, 8))

        self.file_list_label = ctk.CTkLabel(
            container, text="", wraplength=360, justify="left", text_color="gray60", anchor="w"
        )
        self.file_list_label.pack(fill="x", pady=(0, 20))

        strategy_frame = ctk.CTkFrame(container, fg_color="transparent")
        strategy_frame.pack(fill="x", pady=(0, 20))
        self.strategy_label = ctk.CTkLabel(strategy_frame, text="")
        self.strategy_label.pack(side="left")
        self.strategy_menu = ctk.CTkOptionMenu(strategy_frame, width=160, command=self.change_strategy)
        self.strategy_menu.pack(side="right")

        self.compress_button = ctk.CTkButton(
            container, text="", command=self.start_compression, height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.compress_button.pack(fill="x", pady=(0, 8))

        self.status_label = ctk.CTkLabel(container, text="", text_color="gray60")
        self.status_label.pack(pady=(0, 12))

        self.results_label = ctk.CTkLabel(container, text="", anchor="w", text_color="gray60")
        self.results_label.pack(fill="x")
        self.results_box = ctk.CTkTextbox(
            container, height=160, state="disabled",
            border_width=1, border_color="gray30", fg_color=("gray90", "gray17")
        )
        self.results_box.pack(fill="both", expand=True, pady=(4, 0))

    def _apply_language(self):
        t = TEXT[self.language]
        self.title(t["window_title"])
        self.title_label.configure(text=t["title"])
        self.select_button.configure(text=t["select_files"])
        if not self.selected_files:
            self.file_list_label.configure(text=t["no_files"])
        self.strategy_label.configure(text=t["strategy_label"])
        self.compress_button.configure(text=t["compress"])
        self.results_label.configure(text=t["results"])

        strategy_names = list(t["strategies"].values())
        self.strategy_menu.configure(values=strategy_names)
        self.strategy_menu.set(t["strategies"][self.selected_strategy_key])

    def change_language(self, chosen_language):
        self.language = chosen_language
        self._apply_language()

    def change_strategy(self, chosen_label):
        t = TEXT[self.language]
        for key, label in t["strategies"].items():
            if label == chosen_label:
                self.selected_strategy_key = key
                break

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
        if files:
            self.selected_files = [Path(f) for f in files]
            self.file_list_label.configure(text="\n".join(f.name for f in self.selected_files))

    def start_compression(self):
        t = TEXT[self.language]
        if not self.selected_files:
            messagebox.showwarning(t["no_files_title"], t["no_files_message"])
            return

        self.compress_button.configure(state="disabled")
        self.status_label.configure(text=t["compressing"])
        self.results_box.configure(state="normal")
        self.results_box.delete("1.0", "end")
        self.results_box.configure(state="disabled")

        strategy = STRATEGY_OBJECTS[self.selected_strategy_key]
        thread = threading.Thread(target=self.run_compression, args=(strategy,))
        thread.start()

    def run_compression(self, strategy):
        t = TEXT[self.language]
        try:
            results = self.batch.compress_all(self.selected_files, strategy)
        except GhostscriptNotFoundError:
            self.after(0, self.show_error, t["gs_not_found"])
            return

        self.after(0, self.show_results, results)

    def show_results(self, results):
        t = TEXT[self.language]
        self.results_box.configure(state="normal")
        if not results:
            self.results_box.insert("end", t["no_results"])
        else:
            for result in results:
                self.results_box.insert("end", f"{result.output_path.name}: {result}\n")
        self.results_box.configure(state="disabled")
        self.status_label.configure(text=t["done"])
        self.compress_button.configure(state="normal")

    def show_error(self, message):
        t = TEXT[self.language]
        messagebox.showerror(t["error_title"], message)
        self.status_label.configure(text="")
        self.compress_button.configure(state="normal")


if __name__ == "__main__":
    app = PDFCompressorApp()
    app.mainloop()

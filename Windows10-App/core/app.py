import tkinter as tk
from pages.page1 import Page1
from pages.page2 import Page2
from pages.page3 import Page3
import backend.DepotDownloaderHandler as ddhandler
from .verify import verify

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Downloader")
        self.geometry("900x600")

        # container
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.iconbitmap("icon1.ico")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # ✅ TWORZYSZ TYLKO RAZ (TO BYŁ TWÓJ BUG)
        self.page1 = Page1(container, self)
        self.page2 = Page2(container, self)
        self.page3 = Page3(container, self)

        # stack pages
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page3.grid(row=0, column=0, sticky="nsew")

        self.show_page(self.page1)

        # backend callback entry point
        self.download_process = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- NAVIGATION ----------------

    def show_page(self, page):
        verify()
        page.tkraise()

    # ---------------- BACKEND EVENTS ----------------

    def on_backend_event(self, event, data):
        """
        Jedyny punkt wejścia z backendu
        """

        # Page2 always gets raw logs/state
        if hasattr(self, "page2"):
            self.page2._handle_event(event, data)

        # Page3 also gets full updates
        if hasattr(self, "page3"):
            self.page3.handle_event(event, data)

    # ---------------- DOWNLOAD CONTROL ----------------

    def start_download(self, login, password, folder):
        """
        Centralne uruchamianie backendu (ważne!)
        """

        self.download_process, _ = ddhandler.start_download(
            login,
            password,
            folder,
            callback=self.on_backend_event
        )

    # ---------------- CLOSE ----------------

    def on_close(self):
        try:
            if self.download_process:
                ddhandler.stop_download(self.download_process)
        except Exception:
            pass
        self.destroy()
import tkinter as tk
from tkinter import ttk
from pages.page1 import Page1
from pages.page2 import Page2
from pages.page3 import Page3
import backend.DepotDownloaderHandler as ddhandler


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure ttk theme so button colors are controllable on macOS
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure('Primary.TButton', background='#3b82f6', foreground='#ffffff', font=(None, 12, 'bold'))
        style.map('Primary.TButton', background=[('active', '#245fcf'), ('pressed', '#245fcf')], foreground=[('active', '#ffffff')])

        style.configure('Secondary.TButton', background='#2b2b39', foreground='#e6e6e6')
        style.map('Secondary.TButton', background=[('active', '#1f1f28')], foreground=[('active', '#ffffff')])

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.page1 = Page1(container, self)
        self.page2 = Page2(container, self)
        self.page3 = Page3(container, self)

        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page3.grid(row=0, column=0, sticky="nsew")

        self.show_page(self.page1)

        # ensure downloads stop when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_page(self, page):
        page.tkraise()

    def on_close(self):
        # try to stop any running download process before exiting
        try:
            if hasattr(self, 'page2') and getattr(self.page2, 'download_process', None):
                ddhandler.stop_download(self.page2.download_process)
        except Exception:
            pass
        self.destroy()
import tkinter as tk
from tkinter import ttk


class Page1(tk.Frame):
    def __init__(self, master, controller):
        # ciemne tło dla całej strony
        super().__init__(master, bg="#1e1e2f")

        self.controller = controller

        # Centralny kontener z paddingiem
        container = tk.Frame(self, bg="#1e1e2f")
        container.pack(fill="both", expand=True, padx=28, pady=28)

        title = tk.Label(container, text="WELCOME TO SQE4 DOWNLOADER", font=(None, 20, "bold"), bg="#1e1e2f", fg="#ffffff")
        title.pack(pady=(8, 10))

        subtitle = tk.Label(container, text="Installer helper — click NEXT to continue", bg="#1e1e2f", fg="#cbd5e1")
        subtitle.pack(pady=(0, 18))

        btn_frame = tk.Frame(container, bg="#1e1e2f")
        btn_frame.pack()

        next_btn = ttk.Button(btn_frame, text="NEXT", style='Primary.TButton', command=lambda: controller.show_page(controller.page2))
        next_btn.pack(side="left", padx=(0, 8))

        cancel = ttk.Button(btn_frame, text="CANCEL", style='Secondary.TButton', command=master.quit)
        cancel.pack(side="left")
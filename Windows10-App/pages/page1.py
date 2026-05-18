import tkinter as tk
from tkinter import ttk
from core.verify import switch_appdata, VerifySquadAppdata


class Page1(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#0f1220")
        self.controller = controller

        # ================= MAIN =================
        container = tk.Frame(self, bg="#0f1220")
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # ================= TITLE =================
        title = tk.Label(
            container,
            text="SQUAD INSTALLER / DOWNLOADER",
            font=("Segoe UI", 22, "bold"),
            bg="#0f1220",
            fg="#ffffff"
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            container,
            text="Manage AppData version and start download",
            font=("Segoe UI", 11),
            bg="#0f1220",
            fg="#9ca3af"
        )
        subtitle.pack(pady=(0, 25))

        # ================= STATUS CARD =================
        self.card = tk.Frame(container, bg="#1b2035", bd=0, relief="flat")
        self.card.pack(fill="x", pady=(0, 20))

        self.status_label = tk.Label(
            self.card,
            text="Checking AppData...",
            font=("Segoe UI", 12, "bold"),
            bg="#1b2035",
            fg="#ffffff"
        )
        self.status_label.pack(pady=15)

        self.refresh_status()

        # ================= BUTTONS =================
        btn_container = tk.Frame(container, bg="#0f1220")
        btn_container.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=8)

        self.download_btn = ttk.Button(
            btn_container,
            text="⬇ DOWNLOAD SQUAD",
            command=self.go_download
        )
        self.download_btn.grid(row=0, column=0, padx=8)

        self.switch_btn = ttk.Button(
            btn_container,
            text="🔄 SWITCH APPDATA",
            command=self.handle_switch
        )
        self.switch_btn.grid(row=0, column=1, padx=8)

        self.refresh_btn = ttk.Button(
            btn_container,
            text="🔁 REFRESH STATUS",
            command=self.refresh_status
        )
        self.refresh_btn.grid(row=0, column=2, padx=8)

        # ================= FOOTER =================
        footer = tk.Label(
            container,
            text="UE4 / UE5 AppData manager",
            bg="#0f1220",
            fg="#4b5563",
            font=("Segoe UI", 9)
        )
        footer.pack(side="bottom", pady=10)

    # ================= FUNCTIONS =================

    def refresh_status(self):
        try:
            result = VerifySquadAppdata()

            if result == "UE4":
                text = "Current AppData: UE4"
                color = "#fbbf24"
            elif result == "UE5":
                text = "Current AppData: UE5"
                color = "#34d399"
            else:
                text = f"Unknown state: {result}"
                color = "#ef4444"

            self.status_label.config(text=text, fg=color)

        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="#ef4444")

    def handle_switch(self):
        try:
            switch_appdata()
            self.refresh_status()
        except Exception as e:
            self.status_label.config(text=f"Switch error: {e}", fg="#ef4444")

    def go_download(self):
        self.controller.show_page(self.controller.page2)
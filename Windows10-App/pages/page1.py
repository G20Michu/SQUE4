import tkinter as tk
from tkinter import ttk
from core.verify import switch_appdata, VerifySquadAppdata, VerifySquadMod


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

        # APPDATA STATUS
        self.status_label = tk.Label(
            self.card,
            text="Checking AppData...",
            font=("Segoe UI", 12, "bold"),
            bg="#1b2035",
            fg="#ffffff"
        )
        self.status_label.pack(pady=15)

        # MOD STATUS
        self.mod_status_label = tk.Label(
            self.card,
            text="Checking mods...",
            font=("Segoe UI", 10),
            bg="#1b2035",
            fg="#9ca3af"
        )
        self.mod_status_label.pack(pady=(0, 15))

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

        self.refresh_status()

    # ================= FUNCTIONS =================

    def refresh_status(self):
        try:
            # ===== APPDATA =====
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

            # ===== MOD =====
            try:
                status = VerifySquadMod(2428425228)

                if status is True:
                    mod_text = "Mod: Installed ✅"
                    mod_color = "#34d399"
                elif status is False:
                    mod_text = "Mod: Not installed ❌"
                    mod_color = "#ef4444"
                else:
                    mod_text = f"Mod: {status}"
                    mod_color = "#fbbf24"

                self.mod_status_label.config(text=mod_text, fg=mod_color)

            except Exception as e:
                self.mod_status_label.config(
                    text=f"Mod error: {e}",
                    fg="#ef4444"
                )

        except Exception as e:
            self.status_label.config(
                text=f"Error: {e}",
                fg="#ef4444"
            )

    def handle_switch(self):
        try:
            switch_appdata()
            self.refresh_status()
        except Exception as e:
            self.status_label.config(
                text=f"Switch error: {e}",
                fg="#ef4444"
            )

    def go_download(self):
        self.controller.show_page(self.controller.page2)
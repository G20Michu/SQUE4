import tkinter as tk
from tkinter import ttk, filedialog
import backend.DepotDownloaderHandler as ddhandler
import threading
import re
import os
import time


class Page2(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#1e1e2f")
        self.controller = controller
        self._guard_prompt_seen = False  # Flaga do śledzenia potrzeby Steam Guard

        # UI Layout (skrócony dla przejrzystości, zachowaj swoje style)
        container = tk.Frame(self, bg="#1e1e2f")
        container.pack(fill="both", expand=True, padx=28, pady=28)

        # Formularz
        form = tk.Frame(container, bg="#1e1e2f")
        form.pack(fill="x", pady=(0, 12))

        # Login/Hasło
        tk.Label(form, text="Login:", bg="#1e1e2f", fg="#ffffff").grid(row=0, column=0, sticky="w")
        self.login_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.login_var, width=30).grid(row=0, column=1, pady=6, padx=8)

        tk.Label(form, text="Password:", bg="#1e1e2f", fg="#ffffff").grid(row=1, column=0, sticky="w")
        self.password_var = tk.StringVar()
        pwd_entry = ttk.Entry(form, textvariable=self.password_var, show="*", width=30)
        pwd_entry.grid(row=1, column=1, pady=6, padx=8)

        self.login_btn = ttk.Button(form, text="START", command=self.on_login)
        self.login_btn.grid(row=1, column=2, padx=(8, 0))

        # Sekcja Steam Guard (ukryta domyślnie)
        self.guard_label = tk.Label(form, text="Steam Guard:", bg="#1e1e2f", fg="#ffffff")
        self.guard_var = tk.StringVar()
        self.guard_entry = tk.Entry(form, textvariable=self.guard_var, width=20, bg="#2b2b39", fg="#ffffff")
        self.send_guard_btn = tk.Button(form, text="Send Code", bg="#2b2b39", fg="#ffffff", command=self.submit_guard)

        # Folder
        tk.Label(form, text="Folder:", bg="#1e1e2f", fg="#ffffff").grid(row=3, column=0, sticky="w")
        self.folder_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.folder_var, width=40).grid(row=3, column=1, pady=6, padx=8, sticky="ew")
        ttk.Button(form, text="Browse", command=lambda: self.folder_var.set(filedialog.askdirectory())).grid(row=3,
                                                                                                             column=2)

        # Logi
        self.log = tk.Text(container, height=10, bg="#0f1724", fg="#d1d5db", state="disabled")
        self.log.pack(fill="both", expand=True, pady=10)

        self.download_process = None
        self._blink_job = None

    def append_log(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def on_backend_event(self, event, data):
        """Obsługa zdarzeń z wątku backendu w wątku UI."""
        self.after(0, lambda: self._handle_event(event, data))

    def _handle_event(self, event, data):
        if event == "log":
            self.append_log(data)
            # Przekaż do strony statusu (Page3) jeśli istnieje
            if hasattr(self.controller, 'page3'):
                self.controller.page3.append_log(data)

        elif event == "steam_guard":
            self._guard_prompt_seen = True
            self.show_guard_ui()

        elif event == "error":
            self.append_log(f"❌ ERROR: {data}")
            self.stop_blink()

    def show_guard_ui(self):
        self.guard_label.grid(row=2, column=0, sticky="w")
        self.guard_entry.grid(row=2, column=1, pady=6, padx=8, sticky="w")
        self.send_guard_btn.grid(row=2, column=2, padx=(8, 0))
        self.start_blink()
        self.append_log("⚠️ Steam Guard Required! Check your email/app.")

    def submit_guard(self):
        code = self.guard_var.get().strip()
        if code and self.download_process:
            ddhandler.send_guard(self.download_process, code)
            self.stop_blink()
            self.append_log(f"Sent code: {code}")
            # Po wysłaniu kodu, przejdź do strony statusu
            self.controller.show_page(self.controller.page3)

    def on_login(self):
        login = self.login_var.get()
        password = self.password_var.get()
        folder = self.folder_var.get()

        if not all([login, password, folder]):
            self.append_log("Fill all fields!")
            return

        self.append_log("Starting DepotDownloader...")
        self.download_process, _ = ddhandler.start_download(
            login, password, folder, callback=self.on_backend_event
        )

        # Sprawdź po 4 sekundach, czy proces nie potrzebuje Guard (jeśli nie wyłapał eventu wcześniej)
        self.after(4000, self.check_initial_guard)

    def check_initial_guard(self):
        if not self._guard_prompt_seen:
            # Jeśli przez 4 sekundy nie było prośby o Guard, zakładamy sukces logowania
            # i przełączamy widok
            if self.download_process and self.download_process.poll() is None:
                self.controller.show_page(self.controller.page3)

    # --- Animacja migania ---
    def start_blink(self):
        if not self._blink_job: self._blink_cycle()

    def _blink_cycle(self):
        current_bg = self.guard_entry.cget("bg")
        next_bg = "#ffd54f" if current_bg == "#2b2b39" else "#2b2b39"
        self.guard_entry.config(bg=next_bg)
        self.send_guard_btn.config(bg=next_bg)
        self._blink_job = self.after(500, self._blink_cycle)

    def stop_blink(self):
        if self._blink_job:
            self.after_cancel(self._blink_job)
            self._blink_job = None
        self.guard_entry.config(bg="#2b2b39")
        self.send_guard_btn.config(bg="#2b2b39")
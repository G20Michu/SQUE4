import tkinter as tk
from tkinter import ttk, filedialog


class Page2(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#0f1220")
        self.controller = controller

        self._guard_prompt_seen = False

        # ================= ROOT =================
        container = tk.Frame(self, bg="#0f1220")
        container.pack(fill="both", expand=True, padx=25, pady=20)

        # ================= TITLE (CIAŚNIEJ) =================
        title = tk.Label(
            container,
            text="DEPOT DOWNLOADER",
            font=("Segoe UI", 18, "bold"),
            bg="#0f1220",
            fg="#ffffff"
        )
        title.pack(pady=(0, 2))

        subtitle = tk.Label(
            container,
            text="Login, folder and download",
            font=("Segoe UI", 10),
            bg="#0f1220",
            fg="#9ca3af"
        )
        subtitle.pack(pady=(0, 10))

        # ================= LOGIN CARD =================
        card = tk.Frame(container, bg="#1b2035")
        card.pack(fill="x", pady=6)

        inner = tk.Frame(card, bg="#1b2035")
        inner.pack(padx=15, pady=12, fill="x")

        tk.Label(inner, text="Login", bg="#1b2035", fg="white",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")

        self.login_var = tk.StringVar()
        ttk.Entry(inner, textvariable=self.login_var, width=32).grid(
            row=0, column=1, padx=8, pady=3
        )

        tk.Label(inner, text="Password", bg="#1b2035", fg="white",
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w")

        self.password_var = tk.StringVar()
        ttk.Entry(inner, textvariable=self.password_var, show="*", width=32).grid(
            row=1, column=1, padx=8, pady=3
        )

        # ================= FOLDER CARD =================
        folder_card = tk.Frame(container, bg="#1b2035")
        folder_card.pack(fill="x", pady=6)

        inner2 = tk.Frame(folder_card, bg="#1b2035")
        inner2.pack(padx=15, pady=12, fill="x")

        tk.Label(inner2, text="Folder", bg="#1b2035", fg="white",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")

        self.folder_var = tk.StringVar()
        ttk.Entry(inner2, textvariable=self.folder_var, width=34).grid(
            row=0, column=1, padx=8
        )

        ttk.Button(inner2, text="Browse", command=self.pick_folder).grid(row=0, column=2)

        # SHORTCUT
        self.shortcut_var = tk.IntVar(value=0)
        ttk.Checkbutton(
            inner2,
            text="Desktop shortcut",
            variable=self.shortcut_var
        ).grid(row=1, column=1, sticky="w", pady=(5, 0))

        # ================= LOG =================
        log_card = tk.Frame(container, bg="#1b2035")
        log_card.pack(fill="both", expand=True, pady=8)

        self.log = tk.Text(
            log_card,
            height=8,
            bg="#0f1220",
            fg="#d1d5db",
            state="disabled",
            font=("Consolas", 9)
        )
        self.log.pack(fill="both", expand=True, padx=10, pady=8)
        self.guard_popup_open = False
        self.download_clicked = False
        # ================= ERROR =================
        self.login_error_frame = tk.Frame(container, bg="#2a0f14")
        self.login_error_label = tk.Label(
            self.login_error_frame,
            text="",
            bg="#2a0f14",
            fg="#ef4444",
            font=("Segoe UI", 10, "bold")
        )
        self.login_error_label.pack(padx=10, pady=6)

        # ================= DOWNLOAD BUTTON (CIAŚNIEJ + NA DOLE) =================
        self.download_btn = tk.Button(
            container,
            text="DOWNLOAD",
            command=self.on_login,
            state="disabled",
            bg="#2b2b2b",
            fg="#777",
            activebackground="#16a34a",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            height=1
        )
        self.download_btn.pack(fill="x", pady=(8, 0))

        # ================= LIVE VALIDATION =================
        self.login_var.trace_add("write", self._check_form)
        self.password_var.trace_add("write", self._check_form)
        self.folder_var.trace_add("write", self._check_form)


        self._check_form()

    # ================= FORM CHECK =================
    def _check_form(self, *args):
        login = self.login_var.get().strip()
        password = self.password_var.get().strip()
        folder = self.folder_var.get().strip()

        if login and password and folder:
            self.download_btn.config(
                state="normal",
                bg="#22c55e",
                fg="white"
            )
        else:
            self.download_btn.config(
                state="disabled",
                bg="#2b2b2b",
                fg="#777"
            )

    # ================= LOGS =================
    def append_log(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # ================= BACKEND =================
    def on_backend_event(self, event, data):
        self.after(0, lambda: self._handle_event(event, data))

    def show_guard_ui(self):
        if self.guard_popup_open:
            return  # blokada drugiego okna

        self.guard_popup_open = True

        popup = tk.Toplevel(self)
        popup.title("Steam Guard")
        popup.geometry("300x150")

        def on_close():
            self.guard_popup_open = False
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        tk.Label(popup, text="Enter Steam Guard code").pack(pady=10)

        code_var = tk.StringVar()

        entry = ttk.Entry(popup, textvariable=code_var)
        entry.pack()

        def send():
            self.controller.send_guard(code_var.get())
            self.guard_popup_open = False
            popup.destroy()

        ttk.Button(popup, text="Send", command=send).pack(pady=10)

    def _check_if_ready(self):
        return (
                self.login_var.get().strip() and
                self.password_var.get().strip() and
                self.folder_var.get().strip()
        )
    def _handle_event(self, event, data):
        if event == "log":
            self.append_log(data)


        elif event == "steam_guard":

            self._guard_prompt_seen = True

            self.append_log("⚠ Steam Guard required")

            self.show_guard_ui()


        elif event == "error":

            self.append_log(f"❌ {data}")

            self.show_login_error(data)

            # RESET BUTTON (ważne)

            self.download_clicked = False

            self.download_btn.config(

                state="normal",

                bg="#22c55e" if self._check_if_ready() else "#2b2b2b",

                fg="white" if self._check_if_ready() else "#777"

            )

        elif event == "progress":
            if hasattr(self.controller, "page3"):
                self.controller.page3.update_progress(data)

        elif event == "page3":
            self.controller.show_page(self.controller.page3)

    # ================= LOGIN =================
    def on_login(self):
        if self.download_clicked:
            return  # blokada ponownego kliknięcia

        self.download_clicked = True

        self.download_btn.config(
            state="disabled",
            bg="#6b7280",  # szary
            fg="#d1d5db"
        )

        self.append_log("Starting download...")

        self.controller.start_download(
            self.login_var.get(),
            self.password_var.get(),
            self.folder_var.get(),
            create_shortcut=bool(self.shortcut_var.get())
        )

    # ================= FOLDER =================
    def pick_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)

    # ================= ERROR =================
    def show_login_error(self, text):
        self.login_error_label.config(text=text)
        self.login_error_frame.pack(fill="x", pady=(8, 0))
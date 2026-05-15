import tkinter as tk
from tkinter import ttk


class Page3(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#1e1e2f")
        self.controller = controller

        container = tk.Frame(self, bg="#1e1e2f")
        container.pack(fill="both", expand=True, padx=28, pady=28)

        title = tk.Label(
            container,
            text="Download Status",
            font=(None, 18, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        title.pack(pady=(6, 8))

        self.status_label = tk.Label(container, text="Waiting...", bg="#1e1e2f", fg="#cbd5e1")
        self.status_label.pack(pady=(0, 8))

        self.speed_label = tk.Label(container, text="Speed: 0 B/s", bg="#1e1e2f", fg="#cbd5e1")
        self.speed_label.pack(pady=(0, 8))

        # Progress
        self.progress = ttk.Progressbar(container, length=400, mode="determinate")
        self.progress.pack(pady=(12, 6))

        self.percent_label = tk.Label(container, text="0%", bg="#1e1e2f", fg="#cbd5e1")
        self.percent_label.pack()

        self.transferred_label = tk.Label(container, text="0 MB / 0 MB", bg="#1e1e2f", fg="#cbd5e1")
        self.transferred_label.pack(pady=(6, 0))

        # Logs button
        self._logs_visible = False
        self._logs_btn = ttk.Button(container, text="Show logs", command=self._toggle_logs)
        self._logs_btn.pack(pady=(12, 4))

        # Logs frame
        self._logs_frame = tk.Frame(container, bg="#0b1220")

        self._logs_text = tk.Text(
            self._logs_frame,
            height=10,
            bg="#031022",
            fg="#d1d5db",
            state="disabled"
        )

        self._logs_scroll = ttk.Scrollbar(
            self._logs_frame,
            orient="vertical",
            command=self._logs_text.yview
        )

        self._logs_text.configure(yscrollcommand=self._logs_scroll.set)

        self._logs_scroll.pack(side="right", fill="y")
        self._logs_text.pack(side="left", fill="both", expand=True)

    # ---------------- UI SAFE UPDATES ----------------

    def update_status(self, text: str):
        self.after(0, lambda: self.status_label.config(text=text))

    def update_speed(self, text: str):
        self.after(0, lambda: self.speed_label.config(text=f"Speed: {text}"))

    def update_progress(self, percent: float):
        def _update():
            try:
                p = max(0.0, min(100.0, float(percent)))
            except Exception:
                return

            self.progress["value"] = p
            self.percent_label.config(text=f"{p:.2f}%")

        self.after(0, _update)

    def update_transferred(self, transferred_bytes: float, total_bytes: float = None):
        def fmt(b):
            return f"{b / 1024 / 1024:.2f} MB"

        def _update():
            try:
                tr = float(transferred_bytes) if transferred_bytes else 0.0
                tb = float(total_bytes) if total_bytes is not None else None
            except Exception:
                return

            if tb is None or tb == 0:
                self.transferred_label.config(text=f"{fmt(tr)}")
            else:
                self.transferred_label.config(text=f"{fmt(tr)} / {fmt(tb)}")

        self.after(0, _update)

    # ---------------- LOGS ----------------

    def append_log(self, line: str):
        def _update():
            self._logs_text.configure(state="normal")
            self._logs_text.insert("end", line + "\n")
            self._logs_text.see("end")
            self._logs_text.configure(state="disabled")

        self.after(0, _update)

    def clear_logs(self):
        def _update():
            self._logs_text.configure(state="normal")
            self._logs_text.delete("1.0", "end")
            self._logs_text.configure(state="disabled")

        self.after(0, _update)

    # ---------------- TOGGLE ----------------

    def _toggle_logs(self):
        if self._logs_visible:
            self._logs_frame.pack_forget()
            self._logs_btn.config(text="Show logs")
        else:
            self._logs_frame.pack(fill="both", expand=False, pady=(6, 0))
            self._logs_btn.config(text="Hide logs")

        self._logs_visible = not self._logs_visible

    # ---------------- OPTIONAL EVENT ENTRY ----------------

    def handle_event(self, event: str, data):
        """
        Jeśli chcesz mieć pełną integrację (polecam),
        Page3 może sama reagować na backend.
        """

        if event == "log":
            self.append_log(data)

        elif event == "error":
            self.append_log(f"❌ ERROR: {data}")
            self.update_status("ERROR")

        elif event == "steam_guard":
            self.update_status("Steam Guard required")
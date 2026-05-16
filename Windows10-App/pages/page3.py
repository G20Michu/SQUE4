import tkinter as tk
from tkinter import ttk


class Page3(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#0f111a")
        self.controller = controller

        # ================= ROOT =================
        container = tk.Frame(self, bg="#0f111a")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # ================= TITLE =================
        title = tk.Label(
            container,
            text="DOWNLOAD STATUS",
            font=(None, 20, "bold"),
            bg="#0f111a",
            fg="#ffffff"
        )
        title.pack(anchor="w")

        self.status_label = tk.Label(
            container,
            text="Waiting...",
            bg="#0f111a",
            fg="#8b93a7"
        )
        self.status_label.pack(anchor="w", pady=(2, 15))

        # ================= CARD: PROGRESS =================
        progress_card = tk.Frame(container, bg="#151826")
        progress_card.pack(fill="x", pady=10)

        inner = tk.Frame(progress_card, bg="#151826")
        inner.pack(padx=15, pady=15, fill="x")

        self.progress = ttk.Progressbar(inner, length=500, mode="determinate")
        self.progress.pack(fill="x")
        self.progress["maximum"] = 100

        self.percent_label = tk.Label(
            inner,
            text="0%",
            bg="#151826",
            fg="#cbd5e1"
        )
        self.percent_label.pack(anchor="w", pady=(5, 0))


        # ================= ERROR =================
        self.error_frame = tk.Frame(container, bg="#2a0f14")
        self.error_label = tk.Label(
            self.error_frame,
            text="",
            bg="#2a0f14",
            fg="#ff6b6b",
            font=(None, 11, "bold")
        )
        self.error_label.pack(padx=10, pady=8)

        # ================= COMPLETE =================
        self.complete_frame = tk.Frame(container, bg="#0f3d1a")

        self.complete_label = tk.Label(
            self.complete_frame,
            text="Download Complete",
            bg="#0f3d1a",
            fg="#4ade80",
            font=(None, 12, "bold")
        )
        self.complete_label.pack(padx=10, pady=(10, 5))

        self.exit_btn = ttk.Button(
            self.complete_frame,
            text="Exit",
            command=self.controller.quit
        )
        self.exit_btn.pack(pady=(0, 10))

        # ================= LOGS =================
        self._logs_visible = False

        self._logs_btn = ttk.Button(container, text="Show logs", command=self._toggle_logs)
        self._logs_btn.pack(pady=(15, 5))

        self._logs_frame = tk.Frame(container, bg="#151826")

        self._logs_text = tk.Text(
            self._logs_frame,
            height=10,
            bg="#0b0f1a",
            fg="#d1d5db",
            state="disabled"
        )
        self._logs_text.pack(fill="both", expand=True, padx=10, pady=10)

    # =====================================================
    # UPDATE UI
    # =====================================================

    def update_status(self, text: str):
        self.after(0, lambda: self.status_label.config(text=text))

    def update_progress(self, percent: float):
        def _update():
            try:
                p = max(0.0, min(100.0, float(percent)))
            except:
                return

            self.progress["value"] = p
            self.percent_label.config(text=f"{p:.2f}%")

        self.after(0, _update)

    # =====================================================
    # LOGS
    # =====================================================

    def append_log(self, text: str):
        def _update():
            self._logs_text.config(state="normal")
            self._logs_text.insert("end", text + "\n")
            self._logs_text.see("end")
            self._logs_text.config(state="disabled")

        self.after(0, _update)

    def _toggle_logs(self):
        if self._logs_visible:
            self._logs_frame.pack_forget()
            self._logs_btn.config(text="Show logs")
        else:
            self._logs_frame.pack(fill="both", expand=False, pady=(5, 10))
            self._logs_btn.config(text="Hide logs")

        self._logs_visible = not self._logs_visible

    # =====================================================
    # EVENTS
    # =====================================================

    def handle_event(self, event, data):
        if event == "log":
            self.append_log(data)

        elif event == "progress":
            self.update_progress(data)

        elif event == "steam_guard":
            self.update_status("Steam Guard required")

        elif event == "error" and data !="invalid_password" and data!="disk_full":
            self.error_frame.pack(fill="x", pady=(10, 10))
            self.error_label.config(text=str(data))

        elif event == "complete":
            self.update_status("Complete")
            self.progress["value"] = 100
            self.percent_label.config(text="100%")
            self.complete_frame.pack(fill="x", pady=(10, 10))
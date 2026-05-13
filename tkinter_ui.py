import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from pathlib import Path


# ─────────────────────────────────────────────
#  COLOR PALETTE  (dark industrial theme)
# ─────────────────────────────────────────────
BG       = "#1a1a2e"
PANEL    = "#16213e"
ACCENT   = "#e94560"
ACCENT2  = "#0f3460"
FG       = "#eaeaea"
FG_DIM   = "#8892a4"
ENTRY_BG = "#0d1117"
BTN_HV   = "#c73652"
SUCCESS  = "#2ecc71"
WARNING  = "#f39c12"


class CRUDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager – CRUD")
        self.geometry("900x620")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build_ui()
        self.refresh_tree()

    # ─── UI CONSTRUCTION ───────────────────────
    def _build_ui(self):
        self._style()

        # ── Title bar ──
        title_bar = tk.Frame(self, bg=ACCENT2, height=50)
        title_bar.pack(fill="x")
        tk.Label(title_bar, text="⚡  FILE MANAGER  –  CRUD",
                 bg=ACCENT2, fg=FG, font=("Courier New", 14, "bold"),
                 padx=20).pack(side="left", pady=10)

        # ── Main container ──
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=14, pady=10)

        # Left: file tree
        self._build_tree(main)

        # Right: action panel
        self._build_actions(main)

        # Bottom: log console
        self._build_console()

    def _style(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("Treeview",
                      background=PANEL, foreground=FG,
                      fieldbackground=PANEL, rowheight=26,
                      font=("Courier New", 10))
        st.configure("Treeview.Heading",
                      background=ACCENT2, foreground=FG,
                      font=("Courier New", 10, "bold"))
        st.map("Treeview", background=[("selected", ACCENT)])
        st.configure("TScrollbar", background=PANEL, troughcolor=BG,
                      arrowcolor=FG)

    def _build_tree(self, parent):
        left = tk.Frame(parent, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="📁  FILES & FOLDERS",
                 bg=BG, fg=FG_DIM,
                 font=("Courier New", 9, "bold")).pack(anchor="w", pady=(0, 4))

        frame = tk.Frame(left, bg=PANEL, relief="flat", bd=0)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=("type", "size"),
                                  show="headings", selectmode="browse")
        self.tree.heading("type", text="TYPE")
        self.tree.heading("size", text="SIZE")
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("size", width=90, anchor="center")

        # insert a name column visually via the first column trick
        self.tree["columns"] = ("name", "type", "size")
        self.tree.heading("name", text="NAME")
        self.tree.heading("type", text="TYPE")
        self.tree.heading("size", text="SIZE")
        self.tree.column("name", width=240)
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("size", width=90, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_refresh = tk.Button(left, text="⟳  Refresh",
                                 bg=ACCENT2, fg=FG,
                                 font=("Courier New", 9, "bold"),
                                 relief="flat", cursor="hand2",
                                 activebackground=BTN_HV, activeforeground=FG,
                                 command=self.refresh_tree)
        btn_refresh.pack(fill="x", pady=(6, 0))

    def _build_actions(self, parent):
        right = tk.Frame(parent, bg=PANEL, width=260)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="ACTIONS", bg=PANEL, fg=FG_DIM,
                 font=("Courier New", 9, "bold")).pack(pady=(14, 6))

        actions = [
            ("📄  Create File",       self.create_file,   ACCENT),
            ("📖  Read File",         self.read_file,     ACCENT2),
            ("✏️   Update File",       self.update_file,   ACCENT2),
            ("🗑️   Delete File",       self.delete_file,   "#7f1d1d"),
            ("✏️   Rename File",       self.rename_file,   ACCENT2),
            ("📁  Create Folder",     self.create_folder, ACCENT2),
            ("🗂️   Remove Folder",     self.remove_folder, "#7f1d1d"),
            ("📄  File in Folder",    self.create_file_in_folder, ACCENT2),
        ]

        for label, cmd, color in actions:
            b = tk.Button(right, text=label, command=cmd,
                          bg=color, fg=FG,
                          font=("Courier New", 10, "bold"),
                          relief="flat", cursor="hand2",
                          activebackground=BTN_HV, activeforeground=FG,
                          padx=10, pady=8)
            b.pack(fill="x", padx=12, pady=4)

    def _build_console(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(frame, text="CONSOLE LOG",
                 bg=BG, fg=FG_DIM,
                 font=("Courier New", 8, "bold")).pack(anchor="w")

        self.console = scrolledtext.ScrolledText(
            frame, height=6, bg=ENTRY_BG, fg=SUCCESS,
            font=("Courier New", 9), insertbackground=FG,
            relief="flat", state="disabled"
        )
        self.console.pack(fill="x")

    # ─── HELPERS ───────────────────────────────
    def log(self, msg, color=SUCCESS):
        self.console.configure(state="normal")
        self.console.insert("end", f"» {msg}\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        p = Path(".")
        for item in sorted(p.rglob("*")):
            if item.name.startswith("."):
                continue
            kind = "📁 DIR" if item.is_dir() else "📄 FILE"
            try:
                size = f"{item.stat().st_size} B" if item.is_file() else "—"
            except Exception:
                size = "—"
            self.tree.insert("", "end", values=(item, kind, size))
        self.log("Directory refreshed.")

    def _ask(self, prompt, title="Input"):
        return simpledialog.askstring(title, prompt, parent=self)

    def _selected_name(self):
        sel = self.tree.selection()
        if sel:
            return self.tree.item(sel[0])["values"][0]
        return None

    # ─── CRUD OPERATIONS ───────────────────────
    def create_file(self):
        name = self._ask("Enter file name:")
        if not name:
            return
        p = Path(name)
        if p.exists():
            messagebox.showwarning("Exists", f"'{name}' already exists.")
            return
        content = self._ask("Enter file content:") or ""
        p.write_text(content)
        self.log(f"Created file: {name}")
        self.refresh_tree()

    def read_file(self):
        name = self._selected_name() or self._ask("Enter file name to read:")
        if not name:
            return
        p = Path(str(name))
        if not p.exists() or p.is_dir():
            messagebox.showerror("Error", f"'{name}' is not a readable file.")
            return
        content = p.read_text(errors="replace")
        win = tk.Toplevel(self)
        win.title(f"Reading: {name}")
        win.configure(bg=BG)
        win.geometry("600x400")
        tk.Label(win, text=str(name), bg=ACCENT2, fg=FG,
                 font=("Courier New", 11, "bold"),
                 padx=10, pady=6).pack(fill="x")
        txt = scrolledtext.ScrolledText(win, bg=ENTRY_BG, fg=FG,
                                         font=("Courier New", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("end", content)
        txt.configure(state="disabled")
        self.log(f"Read file: {name}")

    def update_file(self):
        name = self._selected_name() or self._ask("Enter file name to update:")
        if not name:
            return
        p = Path(str(name))
        if not p.exists() or p.is_dir():
            messagebox.showerror("Error", f"'{name}' not found.")
            return

        mode_win = tk.Toplevel(self)
        mode_win.title("Update Mode")
        mode_win.configure(bg=BG)
        mode_win.geometry("300x140")
        mode_win.resizable(False, False)
        tk.Label(mode_win, text="Choose update mode:",
                 bg=BG, fg=FG, font=("Courier New", 10)).pack(pady=14)

        def overwrite():
            mode_win.destroy()
            content = self._ask("New content (overwrites existing):")
            if content is not None:
                p.write_text(content)
                self.log(f"Overwritten: {name}")
                self.refresh_tree()

        def append():
            mode_win.destroy()
            content = self._ask("Content to append:")
            if content is not None:
                with open(p, "a") as f:
                    f.write(content)
                self.log(f"Appended to: {name}")
                self.refresh_tree()

        tk.Button(mode_win, text="Overwrite", command=overwrite,
                  bg=ACCENT, fg=FG, font=("Courier New", 10, "bold"),
                  relief="flat", cursor="hand2",
                  padx=10, pady=6).pack(side="left", padx=20, pady=10)
        tk.Button(mode_win, text="Append", command=append,
                  bg=ACCENT2, fg=FG, font=("Courier New", 10, "bold"),
                  relief="flat", cursor="hand2",
                  padx=10, pady=6).pack(side="right", padx=20, pady=10)

    def delete_file(self):
        name = self._selected_name() or self._ask("Enter file name to delete:")
        if not name:
            return
        p = Path(str(name))
        if not p.exists() or p.is_dir():
            messagebox.showerror("Error", f"'{name}' is not a file.")
            return
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            os.remove(p)
            self.log(f"Deleted file: {name}", color=WARNING)
            self.refresh_tree()

    def rename_file(self):
        name = self._selected_name() or self._ask("Enter current file/folder name:")
        if not name:
            return
        p = Path(str(name))
        if not p.exists():
            messagebox.showerror("Error", f"'{name}' does not exist.")
            return
        new_name = self._ask(f"New name for '{name}':")
        if new_name:
            p.rename(new_name)
            self.log(f"Renamed '{name}' → '{new_name}'")
            self.refresh_tree()

    def create_folder(self):
        name = self._ask("Enter folder name:")
        if not name:
            return
        p = Path(name)
        if p.exists():
            messagebox.showwarning("Exists", f"'{name}' already exists.")
            return
        p.mkdir(parents=True)
        self.log(f"Created folder: {name}")
        self.refresh_tree()

    def remove_folder(self):
        name = self._selected_name() or self._ask("Enter folder name to remove:")
        if not name:
            return
        p = Path(str(name))
        if not p.exists() or not p.is_dir():
            messagebox.showerror("Error", f"'{name}' is not a folder.")
            return
        if messagebox.askyesno("Confirm", f"Remove folder '{name}'? (must be empty)"):
            try:
                p.rmdir()
                self.log(f"Removed folder: {name}", color=WARNING)
                self.refresh_tree()
            except OSError as e:
                messagebox.showerror("Error", str(e))

    def create_file_in_folder(self):
        folder = self._ask("Enter existing folder name:")
        if not folder:
            return
        fp = Path(folder)
        if not fp.exists() or not fp.is_dir():
            messagebox.showerror("Error", f"Folder '{folder}' not found.")
            return
        fname = self._ask("Enter new file name:")
        if not fname:
            return
        target = fp / fname
        if target.exists():
            messagebox.showwarning("Exists", f"'{target}' already exists.")
            return
        content = self._ask("Enter file content:") or ""
        target.write_text(content)
        self.log(f"Created '{fname}' inside '{folder}'")
        self.refresh_tree()


if __name__ == "__main__":
    app = CRUDApp()
    app.mainloop()
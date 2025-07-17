# File Integrity Verification Tool
# Developed by: Ashutosh Gautam

import hashlib, os, tkinter as tk
from tkinter import filedialog, messagebox, ttk

ALGORITHMS = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512
}

CHUNK = 64 * 1024

class IntegrityTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Integrity Tool")
        self.geometry("500x350")
        self.configure(bg="#8e8b8b")
        self.path = tk.StringVar()
        self.algo = tk.StringVar(value="SHA-256")
        self.hash_val = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Select File for Integrity Check", fg="white", bg="#5E5B5B").pack(pady=10)
        tk.Entry(self, textvariable=self.path, width=50).pack(pady=5)
        ttk.Button(self, text="Browse", command=self._browse).pack(pady=5)

        tk.Label(self, text="Select Hash Algorithm", fg="white", bg="#767272").pack(pady=10)
        algo_menu = ttk.Combobox(self, textvariable=self.algo, values=list(ALGORITHMS.keys()), state="readonly")
        algo_menu.pack(pady=5)

        ttk.Button(self, text="Generate Hash", command=self._generate_hash).pack(pady=10)
        tk.Entry(self, textvariable=self.hash_val, width=60, state="readonly").pack(pady=5)

        ttk.Button(self, text="Verify Hash", command=self._verify_hash).pack(pady=10)

        self.status = tk.Label(self, text="", fg="white", bg="#a9a2a2")
        self.status.pack(pady=10)

    def _browse(self):
        self.path.set(filedialog.askopenfilename())

    def _generate_hash(self):
        try:
            algo = ALGORITHMS[self.algo.get()]()
            with open(self.path.get(), "rb") as f:
                while chunk := f.read(CHUNK):
                    algo.update(chunk)
            self.hash_val.set(algo.hexdigest())
            self.status.config(text="Hash generated.", fg="green")
        except Exception as e:
            self.status.config(text=f"Error: {e}", fg="red")

    def _verify_hash(self):
        user_hash = tk.simpledialog.askstring("Verify", "Enter the original hash:")
        if not user_hash:
            return
        self._generate_hash()
        match = self.hash_val.get().lower() == user_hash.strip().lower()
        msg = "✔ File is intact." if match else "✖ File has been modified!"
        color = "green" if match else "red"
        messagebox.showinfo("Result", msg)
        self.status.config(text=msg, fg=color)

if __name__ == "__main__":
    IntegrityTool().mainloop()
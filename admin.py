import tkinter as tk
from tkinter import messagebox

class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrator Console")
        self.root.geometry("800x500")
        self.root.configure(bg="lightgrey")

        tk.Label(root, text="Admin Dashboard", font=("Arial", 24, "bold"),
                 bg="lightgrey").pack(pady=30)

        tk.Label(root, text="Manage Factory Settings Here", font=("Arial", 16),
                 bg="lightgrey").pack(pady=10)

        tk.Button(root, text="Exit", font=("Arial", 14, "bold"),
                  bg="#B22222", fg="white", width=12,
                  command=self.exit_program).pack(pady=20)

    def exit_program(self):
        self.root.destroy()
        messagebox.showinfo("Logging Off", "Administrator session closed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root)
    root.mainloop()

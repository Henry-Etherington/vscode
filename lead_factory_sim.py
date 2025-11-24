import tkinter as tk
from tkinter import messagebox

class LeadFactorySimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Lead Engineer Factory Control")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        tk.Label(root, text="Lead Engineer Factory System", font=("Arial", 24, "bold"),
                 bg="white").pack(pady=30)

        tk.Label(root, text="Monitor and Control Factory Lines Here", font=("Arial", 16),
                 bg="white").pack(pady=10)

        tk.Button(root, text="Exit", font=("Arial", 14, "bold"),
                  bg="#B22222", fg="white", width=12,
                  command=self.exit_program).pack(pady=20)

    def exit_program(self):
        self.root.destroy()
        messagebox.showinfo("Logging Off", "Lead Engineer session closed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LeadFactorySimulation(root)
    root.mainloop()


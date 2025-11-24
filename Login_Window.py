import tkinter as tk
from tkinter import messagebox
import os
import Factory_Sim  # Make sure factory_sim.py is in the same folder

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Factory Login")
        self.root.geometry("350x200")
        self.root.resizable(False, False)

        tk.Label(root, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.user_entry = tk.Entry(root, font=("Arial", 12))
        self.user_entry.pack()

        tk.Label(root, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.pass_entry = tk.Entry(root, show="*", font=("Arial", 12))
        self.pass_entry.pack()

        tk.Button(root, text="Login", font=("Arial", 12, "bold"),
                  bg="#2E8B57", fg="white", width=12,
                  command=self.verify_login).pack(pady=15)
        
    def verify_login(self):
        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            login_file = os.path.join(folder, "login.txt")
            if not os.path.exists(login_file):
                messagebox.showerror("Error", "login.txt not found.")
                return

            with open(login_file, "r") as file:
                lines = file.readlines()

            credentials = {}
            for line in lines:
                line = line.strip()
                if ";" in line:
                    user, pwd = line.split(";", 1)
                    credentials[user.strip()] = pwd.strip()

            username = self.user_entry.get().strip()
            password = self.pass_entry.get().strip()

            if username in credentials and credentials[username] == password:
                messagebox.showinfo("Login Successful", "Access Granted.")
                self.root.destroy()

                # Launch FactorySimulation GUI
                main_root = tk.Tk()
                Factory_Sim.FactorySimulation(main_root)
                main_root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        except Exception as e:
            messagebox.showerror("Error", f"Login system error: {e}")

# Entry point for login
if __name__ == "__main__":
    root = tk.Tk()
    # Center the window
    window_width = 350
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)

    LoginWindow(root)
    root.mainloop()

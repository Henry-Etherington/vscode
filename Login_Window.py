import tkinter as tk
from tkinter import messagebox
import os
from factory_sim import FactorySimulation  # import your main factory simulation class

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Factory Login")
        self.root.geometry("350x200")
        self.root.resizable(False, False)

        # Username
        tk.Label(root, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.user_entry = tk.Entry(root, font=("Arial", 12))
        self.user_entry.pack()

        # Password
        tk.Label(root, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.pass_entry = tk.Entry(root, show="*", font=("Arial", 12))
        self.pass_entry.pack()

        # Login Button
        tk.Button(root, text="Login", font=("Arial", 12, "bold"),
                  bg="#2E8B57", fg="white", width=12,
                  command=self.verify_login).pack(pady=15)

    def verify_login(self):
        try:
            # Correct path to login.txt in the same folder as this file
            factory_file = os.path.abspath(__file__)
            factory_folder = os.path.dirname(factory_file)
            login_file = os.path.join(factory_folder, "login.txt")

            if not os.path.exists(login_file):
                messagebox.showerror("Error", "login.txt not found.")
                return

            # Read login credentials
            with open(login_file, "r") as file:
                lines = file.readlines()

            # Parse credentials: format "User;Password"
            credentials = {}
            for line in lines:
                if ";" in line:
                    user, pwd = line.strip().split(";")
                    credentials[user] = pwd

            username = self.user_entry.get().strip()
            password = self.pass_entry.get().strip()

            if username in credentials and credentials[username] == password:
                messagebox.showinfo("Login Successful", "Access Granted.")
                self.root.destroy()  # close login window

                # Launch FactorySimulation
                main_root = tk.Tk()
                FactorySimulation(main_root)
                main_root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        except Exception as e:
            messagebox.showerror("Error", f"Login system error: {e}")

import tkinter as tk
from tkinter import messagebox
import os

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
            folder_path = os.path.dirname(os.path.abspath(__file__))
            login_file = os.path.join(folder_path, "login.txt")

            if not os.path.exists(login_file):
                messagebox.showerror("Error", f"login.txt not found in {folder_path}")
                return

            with open(login_file, "r") as file:
                lines = file.readlines()

            # Expected format: User;Password,Role
            credentials = {}  # username -> (password, role)
            for line in lines[1:]:  # skip header line
                line = line.strip()
                if ";" in line and "," in line:
                    user_pass, role = line.split(",", 1)
                    user, pwd = user_pass.split(";", 1)
                    credentials[user.strip().lower()] = (pwd.strip().lower(), role.strip().lower())

            username_input = self.user_entry.get().strip().lower()
            password_input = self.pass_entry.get().strip().lower()

            if username_input in credentials:
                stored_pwd, role = credentials[username_input]
                if password_input == stored_pwd:
                    messagebox.showinfo("Login Successful", f"Access Granted as {role.capitalize()}")
                    self.root.destroy()

                    # Launch correct system based on role
                    import sys
                    if role == "administrator":
                        import admin
                        main_root = tk.Tk()
                        admin.AdminApp(main_root)
                        main_root.mainloop()
                    elif role == "engineer":
                        import factory_sim
                        main_root = tk.Tk()
                        factory_sim.FactorySimulation(main_root, username_input.capitalize())
                        main_root.mainloop()
                    elif role == "lead engineer":
                        import lead_factory_sim
                        main_root = tk.Tk()
                        lead_factory_sim.LeadFactorySimulation(main_root)
                        main_root.mainloop()
                    else:
                        messagebox.showerror("Error", "Unknown role.")
                else:
                    messagebox.showerror("Login Failed", "Invalid password.")
            else:
                messagebox.showerror("Login Failed", "Invalid username.")

        except Exception as e:
            messagebox.showerror("Error", f"Login system error: {e}")

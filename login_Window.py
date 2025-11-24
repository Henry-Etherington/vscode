import tkinter as tk
from tkinter import messagebox
import os
import sys
import importlib

# Ensure the current folder is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Factory Login")
        self.root.geometry("350x200")
        self.root.resizable(False, False)

        # Username Label & Entry
        tk.Label(root, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.user_entry = tk.Entry(root, font=("Arial", 12))
        self.user_entry.pack()

        # Password Label & Entry
        tk.Label(root, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.pass_entry = tk.Entry(root, show="*", font=("Arial", 12))
        self.pass_entry.pack()

        # Login Button
        tk.Button(
            root,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#2E8B57",
            fg="white",
            width=12,
            command=self.verify_login
        ).pack(pady=15)

    def verify_login(self):
        try:
            # Path to login.txt
            folder_path = os.path.dirname(os.path.abspath(__file__))
            login_file = os.path.join(folder_path, "login.txt")

            if not os.path.exists(login_file):
                messagebox.showerror("Error", f"login.txt not found in {folder_path}")
                return

            # Read credentials
            with open(login_file, "r") as file:
                lines = file.readlines()

            credentials = {}
            for line in lines[1:]:  # skip header
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
                    self.root.withdraw()  # hide login window

                    # Map role to module and class
                    role_map = {
                        "administrator": ("admin", "AdminApp"),
                        "engineer": ("factory_sim", "FactorySimulation"),
                        "lead engineer": ("lead_factory_sim", "LeadFactorySimulation")
                    }

                    if role not in role_map:
                        messagebox.showerror("Error", f"Unknown role '{role}'")
                        return

                    module_name, class_name = role_map[role]

                    try:
                        role_module = importlib.import_module(module_name)
                    except ModuleNotFoundError:
                        messagebox.showerror("Error", f"Module '{module_name}.py' not found")
                        return

                    role_class = getattr(role_module, class_name, None)
                    if not role_class:
                        messagebox.showerror("Error", f"Class '{class_name}' not found in module '{module_name}'")
                        return

                    # Launch the role-specific GUI
                    role_class(tk.Toplevel(self.root))

                else:
                    messagebox.showerror("Login Failed", "Invalid password.")
            else:
                messagebox.showerror("Login Failed", "Invalid username.")

        except Exception as e:
            messagebox.showerror("Error", f"Login system error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

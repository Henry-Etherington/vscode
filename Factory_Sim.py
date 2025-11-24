import tkinter as tk
from tkinter import messagebox
import random
import time
import os
from Login_Window import LoginWindow  # Import the login system

class FactorySimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Autodesk: Factory")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        # GUI size and positioning
        width, height = 900, 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

        # Factory config
        self.max_products = 48
        self.product_count = 0
        self.products = []  # list of tuples: (number, color, timestamp)
        self.product_colors = ["red", "blue", "yellow"]
        self.product_catalog = {"red": "Cooling Unit",
                                "blue": "Emergency Module",
                                "yellow": "Battery Pack"}
        self.production_running = False
        self.warehouse_full_shown = False

        # Title label at top
        self.title_label = tk.Label(self.root, text="Autodesk: Factory",
                                    font=("Arial", 32, "bold"),
                                    bg="black", fg="white")
        self.title_label.pack(pady=10)

        # Legend label below canvas
        legend_text = "  ".join([f"{name}: {color}" for color, name in self.product_catalog.items()])
        self.legend_label = tk.Label(self.root,
                                     text=f"{legend_text}    |    Total Produced: {self.product_count}",
                                     font=("Arial", 12, "bold"),
                                     bg="black", fg="white")
        self.legend_label.pack(pady=5)

        # Canvas for products
        self.canvas = tk.Canvas(root, width=850, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Buttons
        button_frame1 = tk.Frame(root, bg="black")
        button_frame1.pack(pady=5)
        button_frame2 = tk.Frame(root, bg="black")
        button_frame2.pack(pady=5)

        # Start / Stop / Reset / Live / Info / Save / All / Exit buttons
        self.start_btn = tk.Button(button_frame1, text="Start Production", font=("Arial", 14, "bold"),
                                   width=18, height=2, bg="#2E8B57", fg="white",
                                   command=self.start_production)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(button_frame1, text="Stop Production", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#FFA500", fg="white",
                                  command=self.stop_production)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(button_frame1, text="Reset Production", font=("Arial", 14, "bold"),
                                   width=18, height=2, bg="#FFA500", fg="white",
                                   command=self.reset_production)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.live_btn = tk.Button(button_frame2, text="Live Products", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#6A5ACD", fg="white",
                                  command=self.show_live_products)
        self.live_btn.pack(side=tk.LEFT, padx=5)

        self.info_btn = tk.Button(button_frame2, text="Information", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#4B0082", fg="white",
                                  command=self.show_information)
        self.info_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(button_frame2, text="Save Production", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#1E90FF", fg="white",
                                  command=self.save_production)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.all_saved_btn = tk.Button(button_frame2, text="All Saved Products", font=("Arial", 14, "bold"),
                                       width=18, height=2, bg="#1E90FF", fg="white",
                                       command=self.show_all_saved_products)
        self.all_saved_btn.pack(side=tk.LEFT, padx=5)

        self.exit_btn = tk.Button(button_frame2, text="Exit", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#B22222", fg="white",
                                  command=self.exit_program)
        self.exit_btn.pack(side=tk.LEFT, padx=5)

    # --- Produce Product ---
    def produce_product(self):
        if self.product_count >= self.max_products:
            if not self.warehouse_full_shown:
                messagebox.showinfo("Warehouse Full", "Maximum warehouse capacity reached. Stopping production!")
                self.warehouse_full_shown = True
            self.production_running = False
            return
        color = random.choice(self.product_colors)
        timestamp = time.time()
        self.products.append((self.product_count + 1, color, timestamp))
        self.product_count += 1

        # Arrange products in grid
        cols = 12
        spacing_x = 60
        spacing_y = 60
        square_size = 40
        margin_x = 20
        margin_y = 20

        row = (self.product_count - 1) // cols
        col = (self.product_count - 1) % cols

        x1 = margin_x + col * spacing_x
        y1 = margin_y + row * spacing_y
        x2 = x1 + square_size
        y2 = y1 + square_size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2,
                                text=str(self.product_count), fill="white", font=("Arial", 10, "bold"))

        legend_text = "  ".join([f"{name}: {color}" for color, name in self.product_catalog.items()])
        self.legend_label.config(text=f"{legend_text}    |    Total Produced: {self.product_count}")

        print(f"Produced {self.product_catalog[color]} at {time.ctime(timestamp)}")

    # --- Start / Stop / Reset / Save / Live / Info / Exit ---
    def start_production(self):
        if self.production_running:
            messagebox.showinfo("Production Already Running", "Production is already running!")
            return
        self.production_running = True
        messagebox.showinfo("Production Started", "Production has started!")
        self.schedule_production()

    def schedule_production(self):
        if self.production_running:
            self.produce_product()
            self.root.after(1000, self.schedule_production)

    def stop_production(self):
        self.production_running = False
        messagebox.showinfo("Production Stopped", "Production has been stopped.")

    def reset_production(self):
        if self.products:
            answer = messagebox.askyesno("Reset Production", "Warning: Unsaved products will be lost!\nDo you want to continue?")
            if not answer:
                return
        self.products.clear()
        self.product_count = 0
        self.canvas.delete("all")
        self.warehouse_full_shown = False
        legend_text = "  ".join([f"{name}: {color}" for color, name in self.product_catalog.items()])
        self.legend_label.config(text=f"{legend_text}    |    Total Produced: {self.product_count}")
        messagebox.showinfo("Reset", "Production session has been reset.")

    # ... include all other methods like save_production, show_live_products, show_information, show_all_saved_products ...

    def exit_program(self):
        self.root.destroy()
        messagebox.showinfo("Logging Off", "Exiting Factory Simulation.")

# --- Main Launcher ---
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)  # Show login window first
    root.mainloop()

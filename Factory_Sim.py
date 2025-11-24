import tkinter as tk
from tkinter import messagebox
import random
import time
import os

class FactorySimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Autodesk: Factory") 
        self.warehouse_full_notified = False

         # Window bar title

        # GUI size and position
        width, height = 900, 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.configure(bg="black")
        root.resizable(False, False)

        # --- Factory Config ---
        self.max_products = 98 # maximum products in warehouse since warehouse has limited space.
        self.product_count = 0
        self.warehouse_full_shown = False
        self.products = []  # list of tuples: (number, color, timestamp)
        self.product_colors = ["red", "blue", "yellow"]
        self.product_catalog = {"red": "Cooling Unit", 
                                "blue": "Emergency Module", 
                                "yellow": "Battery Pack"}
        self.production_running = False

        # --- GUI Heading above canvas ---
        self.title_label = tk.Label(self.root,
                                    text="Autodesk: Factory",
                                    font=("Arial", 32, "bold"),
                                    bg="black", fg="white")
        self.title_label.pack(pady=10)

        # --- Canvas for products ---
        self.canvas = tk.Canvas(root, width=850, height=400, bg="white")
        self.canvas.pack(pady=10)

        # --- Product Legend & Total Produced Counter (below canvas) ---
        legend_text = "  ".join([f"{name}: {color}" for color, name in self.product_catalog.items()])
        self.legend_label = tk.Label(self.root,
                                     text=f"{legend_text}    |    Total Produced: {self.product_count}",
                                     font=("Arial", 12, "bold"),
                                     bg="black", fg="white")
        self.legend_label.pack(pady=5)

        # --- Buttons ---
        button_frame1 = tk.Frame(root, bg="black")
        button_frame1.pack(pady=5)
        button_frame2 = tk.Frame(root, bg="black")
        button_frame2.pack(pady=5)

        # Start Production
        self.start_btn = tk.Button(button_frame1, text="Start Production", font=("Arial", 14, "bold"),
                                   width=18, height=2, bg="#2E8B57", fg="white",
                                   command=self.start_production)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        # Stop Production
        self.stop_btn = tk.Button(button_frame1, text="Stop Production", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#FFA500", fg="white",
                                  command=self.stop_production)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Reset Production
        self.reset_btn = tk.Button(button_frame1, text="Reset Production", font=("Arial", 14, "bold"),
                                   width=18, height=2, bg="#FFA500", fg="white",
                                   command=self.reset_production)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        # Live Products (last 10)
        self.live_btn = tk.Button(button_frame2, text="Live Products", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#6A5ACD", fg="white",
                                  command=self.show_live_products)
        self.live_btn.pack(side=tk.LEFT, padx=5)

        # Information (Histogram & Pie Chart)
        self.info_btn = tk.Button(button_frame2, text="Information", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#4B0082", fg="white",
                                  command=self.show_information)
        self.info_btn.pack(side=tk.LEFT, padx=5)

        # Save Production
        self.save_btn = tk.Button(button_frame2, text="Save Production", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#1E90FF", fg="white",
                                  command=self.save_production)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # All Saved Products
        self.all_saved_btn = tk.Button(button_frame2, text="All Saved Products", font=("Arial", 14, "bold"),
                                       width=18, height=2, bg="#1E90FF", fg="white",
                                       command=self.show_all_saved_products)
        self.all_saved_btn.pack(side=tk.LEFT, padx=5)

        # Exit
        self.exit_btn = tk.Button(button_frame2, text="Exit", font=("Arial", 14, "bold"),
                                  width=18, height=2, bg="#B22222", fg="white",
                                  command=self.exit_program)
        self.exit_btn.pack(side=tk.LEFT, padx=5)

    # --- Produce Product ---
    def produce_product(self):
        
        """Produce a product and display it as a colored square on the canvas."""
        if self.product_count >= self.max_products:
           if not self.warehouse_full_notified: 
              messagebox.showinfo("Warehouse Full", "Maximum warehouse capacity reached. Stopping production!")
              self.warehouse_full_notified = True
              self.production_running = False
           return

        color = random.choice(self.product_colors)
        timestamp = time.time()
        self.products.append((self.product_count + 1, color, timestamp))
        self.product_count += 1

        # Arrange products in grid
        cols = 14
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

        # Update legend below canvas
        legend_text = "  ".join([f"{name}: {color}" for color, name in self.product_catalog.items()])
        self.legend_label.config(text=f"{legend_text}    |    Total Produced: {self.product_count}")

        print(f"Produced {self.product_catalog[color]} at {time.ctime(timestamp)}")

    # --- Start Production ---
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

    # --- Stop Production ---
    def stop_production(self):
        self.production_running = False
        messagebox.showinfo("Production Stopped", "Production has been stopped.")

    # --- Reset Production ---
    def reset_production(self):
        if self.products:
            answer = messagebox.askyesno(
                "Reset Production",
                "Warning: Unsaved products will be lost!\nDo you want to continue?"
            )
            if not answer:
                return
        self.products.clear()
        self.product_count = 0
        self.canvas.delete("all")
        legend_text = "  ".join([f"{name}: {color}" for color, name in self.product_catalog.items()])
        self.legend_label.config(text=f"{legend_text}    |    Total Produced: {self.product_count}")
        messagebox.showinfo("Reset", "Production session has been reset.")

    # --- Save Production ---
    def save_production(self):
        try:
            folder_path = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(folder_path, "factory_simulation_products.txt")
            with open(filename, "a") as file:
                for prod_num, color, timestamp in self.products:
                    file.write(f"Produced {self.product_catalog[color]} at {time.ctime(timestamp)}\n")
            messagebox.showinfo("Saved", "Production saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save production: {e}")

    # --- Show Live Products ---
    def show_live_products(self):
        window = tk.Toplevel(self.root)
        window.title("Live Products (Last 10)")
        window.geometry("400x300")
        window.configure(bg="white")
        text_area = tk.Text(window, wrap="word", font=("Arial", 12), bg="#f8f8f8", fg="black")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        def update_live_list():
            last_10 = self.products[-10:]
            text_area.config(state="normal")
            text_area.delete("1.0", tk.END)
            for prod_num, color, timestamp in last_10:
                text_area.insert("end", f"Produced {self.product_catalog[color]} at {time.ctime(timestamp)}\n")
            text_area.config(state="disabled")
            window.after(1000, update_live_list)

        update_live_list()

        close_btn = tk.Button(window, text="Close", bg="#B22222", fg="white",
                              font=("Arial", 12, "bold"), command=window.destroy)
        close_btn.pack(pady=5)

    # --- Show Information (Histogram + Pie Chart) ---
    def show_information(self):
     if not self.products:
        messagebox.showinfo("No Data", "No products have been produced yet.")
        return

     window = tk.Toplevel(self.root)
     window.title("Production Information (Live)")
     window.geometry("700x500")  # fixed size
     window.resizable(False, False)  # prevent resizing
     window.configure(bg="white")

     # Canvas for charts
     canvas = tk.Canvas(window, width=680, height=400, bg="#f8f8f8")
     canvas.pack(padx=10, pady=10)

     canvas.create_text(340, 20, text="Histogram & Pie Chart", font=("Arial", 16, "bold"))

     def update_charts():
        canvas.delete("chart")
        counts = {}
        for _, color, _ in self.products:
            counts[color] = counts.get(color, 0) + 1
        total = sum(counts.values())

        # Histogram
        bar_width = 50
        spacing = 40
        max_height = 400
        start_x = 50
        base_y = 300

        for i, color in enumerate(self.product_colors):
            count = counts.get(color, 0)
            height = (count / max(total, 1)) * max_height
            x1 = start_x + i*(bar_width + spacing)
            y1 = base_y - height
            x2 = x1 + bar_width
            y2 = base_y

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="chart")
            canvas.create_text((x1+x2)/2, y1-10, text=f"{count}", font=("Arial", 10), tags="chart")
            canvas.create_text((x1+x2)/2, base_y+15, text=self.product_catalog[color], font=("Arial", 10), tags="chart")

        # Pie chart
        pie_x, pie_y, pie_radius = 520, 120, 80
        start_angle = 0

        for color in self.product_colors:
            count = counts.get(color, 0)
            extent = (count / max(total, 1)) * 360
            if extent > 0:
                canvas.create_arc(pie_x - pie_radius, pie_y - pie_radius,
                                  pie_x + pie_radius, pie_y + pie_radius,
                                  start=start_angle, extent=extent, fill=color, tags="chart")
                # display product name + count
                import math
                mid_angle = start_angle + extent / 2
                rad = math.radians(mid_angle)
                text_x = pie_x + 0.6*pie_radius * math.cos(rad)
                text_y = pie_y - 0.6*pie_radius * math.sin(rad)
                canvas.create_text(text_x, text_y, text=f"{self.product_catalog[color]} ({count})",
                                   font=("Arial", 9), tags="chart")
                start_angle += extent

        window.after(1000, update_charts)

     update_charts()

     # Close button inside window
     close_btn = tk.Button(window, text="Close",
                          bg="#B22222", fg="white",
                          font=("Arial", 14, "bold"),
                          width=20, height=2,
                          command=window.destroy)
     close_btn.pack(pady=5)


    # --- Show All Saved Products ---
    def show_all_saved_products(self):
        folder_path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(folder_path, "factory_simulation_products.txt")

        if not os.path.exists(filename):
            messagebox.showinfo("File Not Found", "No production file found.")
            return

        try:
            with open(filename, "r") as file:
                contents = file.read()

            window = tk.Toplevel(self.root)
            window.title("All Saved Products")
            window.geometry("600x400")
            window.configure(bg="white")

            text_area = tk.Text(window, wrap="word", font=("Arial", 12), bg="#f8f8f8", fg="black")
            text_area.pack(expand=True, fill="both", padx=10, pady=10)
            text_area.insert("1.0", contents)
            text_area.config(state="disabled")

            close_btn = tk.Button(window, text="Close", bg="#B22222", fg="white",
                                  font=("Arial", 12, "bold"), command=window.destroy)
            close_btn.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    # --- Exit Program ---
    def exit_program(self):
        self.root.destroy()
        messagebox.showinfo("Logging Off", "Exiting Factory Simulation.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FactorySimulation(root)
    root.mainloop()

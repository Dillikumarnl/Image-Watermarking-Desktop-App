import tkinter as tk
from app import WatermarkApp


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
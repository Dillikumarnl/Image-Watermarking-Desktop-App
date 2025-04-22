import time
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import ImageTk
from image_processor import ImageProcessor

# GUI class for handling user interface
class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermarking Application")
        self.root.geometry("900x800")
        self.root.config(bg="#9DC3F4")
        self.root.iconbitmap()


        # Initialize image processor
        self.processor = ImageProcessor()


        # Image Selection
        self.image_frame = ttk.Frame(root)
        self.image_frame.pack(pady=20, padx=10)

        self.browse_button = tk.Button(self.image_frame, text="Browse Image", command=self.select_image,
                                       foreground="#658B56", )
        self.browse_button.pack(side=tk.LEFT, padx=5)

        self.selected_image_label = ttk.Label(self.image_frame, text="No image selected", foreground='red')
        self.selected_image_label.pack(side=tk.LEFT, padx=5)


        # Preview Canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="lightgray")
        self.canvas.pack(padx=20, pady=10)


        # Watermark Input
        self.watermark_frame = tk.Frame(root, bg="#EFE651")
        self.watermark_frame.pack(pady=10)

        self.watermark_label = tk.Label(self.watermark_frame, text="Watermark Text:", bg="#658B56", foreground="white")
        self.watermark_label.pack(side=tk.LEFT, padx=5)

        self.watermark_entry = tk.Entry(self.watermark_frame, width=30)
        self.watermark_entry.pack(side=tk.LEFT, padx=5)



        # Position Fixing
        self.position_frame = tk.Frame(root, bg="#F8BB5E")
        self.position_frame.pack(pady=10)

        self.position_label = tk.Label(self.position_frame, text="Position:", bg="#F8BB5E")
        self.position_label.pack(side=tk.LEFT, padx=5)

        self.position_var = tk.StringVar(value="Center")
        self.positions = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"]
        for pos in self.positions:
            rb = ttk.Radiobutton(self.position_frame, text=pos, variable=self.position_var, value=pos)
            rb.pack(side=tk.LEFT)

        # transparency and Size
        self.settings_frame = ttk.Frame(root)
        self.settings_frame.pack(pady=10)

        self.transparency_label = tk.Label(self.settings_frame, text="Transparency:")
        self.transparency_label.pack(side=tk.LEFT, padx=5)

        self.transparency_scale = ttk.Scale(self.settings_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.transparency_scale.set(20)  # Default value
        self.transparency_scale.pack(side=tk.LEFT, padx=5)

        self.size_label = tk.Label(self.settings_frame, text="Size:")
        self.size_label.pack(side=tk.LEFT, padx=5)

        self.size_scale = ttk.Scale(self.settings_frame, from_=50, to=300, orient=tk.HORIZONTAL)
        self.size_scale.set(40)  # Default value
        self.size_scale.pack(side=tk.LEFT, padx=5)

        # Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        self.apply_button = ttk.Button(self.button_frame, text="Apply Watermark", command=self.add_watermark)
        self.apply_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)


    def select_image(self):
        """Select an image file to load."""
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if image_path:
            self.selected_image_label.config(text=image_path, foreground='green')
            self.canvas.config(bg='#9DC3F4', highlightbackground="#9DC3F4")
            self.processor.load_image(image_path)
            self.show_preview(self.processor.get_watermarked_image())


    def show_preview(self, image):
        """Display the preview of the image."""
        if image is None:
            print("Error: No image to display.")
            return

        preview_image = image.copy()
        preview_image.thumbnail((600, 400))
        img_tk = ImageTk.PhotoImage(preview_image)
        self.canvas.image = img_tk
        self.canvas.create_image(300, 200, image=img_tk)

    def add_watermark(self):
        """Add watermark to the image."""
        text = self.watermark_entry.get()
        position = self.position_var.get()
        font_size = int(self.size_scale.get())
        transparency = self.transparency_scale.get()

        # Apply watermark
        self.processor.apply_watermark(text, position, font_size, transparency)
        self.show_preview(self.processor.get_watermarked_image())


    def save_image(self):
        """Save the watermarked image."""
        watermarked_image = self.processor.get_watermarked_image()
        if watermarked_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                watermarked_image.save(save_path)


from PIL import Image, ImageDraw, ImageFont


# Base class for image processing
class ImageProcessor:
    def __init__(self):
        self.image = None
        self.watermarked_image = None

    def load_image(self, image_path):
        """Load an image from the given path."""
        try:
            self.image = Image.open(image_path)
            self.watermarked_image = self.image.copy()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = None
            self.watermarked_image = None

    def apply_watermark(self, text, position, font_size, transparency):
        """Apply watermark to the image."""
        if not self.image:
            return

        # Create a copy of the image to apply watermark
        self.watermarked_image = self.image.copy()
        draw = ImageDraw.Draw(self.watermarked_image)


        try:
            font = ImageFont.truetype("arial.ttf",  font_size)
        except IOError:
            font = ImageFont.load_default()

        # Get bounding box to calculate text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        positions = {
            "Top-Left": (20, 20),
            "Top-Right": (self.watermarked_image.width - text_width - 20, 20),
            "Bottom-Left": (20, self.watermarked_image.height - text_height - 20),
            "Bottom-Right": (self.watermarked_image.width - text_width - 20, self.watermarked_image.height - text_height - 20),
            "Center": ((self.watermarked_image.width - text_width) // 2, (self.watermarked_image.height - text_height) // 2),
        }

        watermark_position = positions.get(position, (20, 20))

        # Apply the watermark with transparency
        draw.text(watermark_position, text, (255, 255, 255, int(transparency)), font=font)


    def get_watermarked_image(self):
        """Return the watermarked image or None if not available."""
        return self.watermarked_image

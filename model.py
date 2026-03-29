from reportlab.lib.pagesizes import A4, letter, legal
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os
import tempfile

# Page sizes
PAGE_SIZES = {
    "A4": A4,
    "Letter": letter,
    "Legal": legal,
    "Original": None
}

def images_to_pdf(uploaded_files, page_size="A4", orientation="Portrait", quality="High", enable_compression=True):
    if not uploaded_files:
        return None, "Koi image upload nahi ki gayi!"

    try:
        quality_map = {"Low": 60, "Medium": 75, "High": 85, "Maximum": 95}
        save_quality = quality_map.get(quality, 85)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            pdf_path = tmp.name

        c = canvas.Canvas(pdf_path)

        for uploaded_file in uploaded_files:
            # PIL Image for size calculation
            pil_img = Image.open(uploaded_file).convert("RGB")
            img_width, img_height = pil_img.size
            img_reader = ImageReader(uploaded_file)

            if page_size == "Original":
                # Original image size
                page_w, page_h = img_width, img_height
                draw_w, draw_h = img_width, img_height
                x, y = 0, 0
            else:
                base_size = PAGE_SIZES[page_size]
                
                # Set orientation
                if orientation == "Landscape":
                    page_size_tuple = landscape(base_size)
                else:
                    page_size_tuple = portrait(base_size)   # ya simply base_size for portrait
                
                page_w, page_h = page_size_tuple

                # Scale image to fit page (maintain aspect ratio)
                scale = min(page_w / img_width, page_h / img_height) * 0.98  # thoda margin ke liye
                draw_w = img_width * scale
                draw_h = img_height * scale

                # Center the image
                x = (page_w - draw_w) / 2
                y = (page_h - draw_h) / 2

            # Set page size and draw image
            c.setPageSize((page_w, page_h))
            c.drawImage(img_reader, x, y, width=draw_w, height=draw_h, 
                       preserveAspectRatio=True, anchor='c')

            c.showPage()   # Next page

        c.save()

        # Read bytes for download
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        os.unlink(pdf_path)

        return pdf_bytes, f"✅ {len(uploaded_files)} images PDF mein convert ho gayi! (Orientation Fixed)"

    except Exception as e:
        return None, f"Conversion error: {str(e)}"

import os
import tempfile
import json
from PIL import Image
import fitz  # PyMuPDF for compression
from PyPDF2 import PdfMerger

# ReportLab imports for better PDF creation with orientation support
from reportlab.lib.pagesizes import A4, letter, legal
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Page sizes dictionary
PAGE_SIZES = {
    "A4": A4,
    "Letter": letter,
    "Legal": legal,
    "Original": None
}

# ====================== Images to PDF (Fixed Landscape + Fit) ======================
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
            # Open image
            pil_img = Image.open(uploaded_file).convert("RGB")
            img_width, img_height = pil_img.size
            img_reader = ImageReader(uploaded_file)

            if page_size == "Original":
                # Use original image size
                page_w, page_h = img_width, img_height
                draw_w, draw_h = img_width, img_height
                x, y = 0, 0
            else:
                base_size = PAGE_SIZES[page_size]
                
                # Apply orientation
                if orientation == "Landscape":
                    page_size_tuple = landscape(base_size)
                else:
                    page_size_tuple = portrait(base_size)

                page_w, page_h = page_size_tuple

                # Scale image to fit page while keeping aspect ratio
                scale = min(page_w / img_width, page_h / img_height) * 0.98
                draw_w = img_width * scale
                draw_h = img_height * scale

                # Center the image on page
                x = (page_w - draw_w) / 2
                y = (page_h - draw_h) / 2

            # Set page size and draw image
            c.setPageSize((page_w, page_h))
            c.drawImage(img_reader, x, y, width=draw_w, height=draw_h, 
                       preserveAspectRatio=True, anchor='c')

            c.showPage()  # Move to next page

        c.save()

        # Read PDF bytes for download
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        os.unlink(pdf_path)

        return pdf_bytes, f"✅ {len(uploaded_files)} images successfully converted to PDF!"

    except Exception as e:
        return None, f"Conversion error: {str(e)}"


# ====================== Merge PDFs ======================
def merge_pdfs(uploaded_pdfs):
    if len(uploaded_pdfs) < 2:
        return None, "Merge karne ke liye kam se kam 2 PDFs upload karein!"

    try:
        merger = PdfMerger()
        temp_paths = []

        for pdf_file in uploaded_pdfs:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_file.getvalue())
                temp_paths.append(tmp.name)
                merger.append(tmp.name)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name

        merger.write(output_path)
        merger.close()

        with open(output_path, "rb") as f:
            merged_bytes = f.read()

        # Cleanup
        os.unlink(output_path)
        for p in temp_paths:
            if os.path.exists(p):
                os.unlink(p)

        return merged_bytes, f"✅ {len(uploaded_pdfs)} PDFs successfully merge ho gaye!"

    except Exception as e:
        return None, f"Merge error: {str(e)}"


# ====================== Compress PDF ======================
def compress_pdf(uploaded_pdf, compression_level="Balanced (Good Quality + Small Size)"):
    if not uploaded_pdf:
        return None, "PDF upload karein!", ""

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_pdf.getvalue())
            input_path = tmp.name

        doc = fitz.open(input_path)
        output_path = input_path.replace(".pdf", "_compressed.pdf")

        for page in doc:
            page.clean_contents()

        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

        with open(output_path, "rb") as f:
            compressed_bytes = f.read()

        # Cleanup
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)

        return compressed_bytes, "✅ PDF successfully compressed!", ""

    except Exception as e:
        return None, f"Compression error: {str(e)}", ""


# ====================== Feedback System ======================
FEEDBACK_FILE = "feedbacks.json"

def load_feedbacks():
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_feedbacks(feedbacks):
    try:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(feedbacks, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def save_feedback(name, feedback_text, rating):
    if not feedback_text or not feedback_text.strip():
        return "❌ Feedback likhna zaroori hai!"

    feedbacks = load_feedbacks()
    feedbacks.append({
        "name": name.strip() if name and name.strip() else "Anonymous",
        "feedback": feedback_text.strip(),
        "rating": rating
    })
    save_feedbacks(feedbacks)
    return "✅ Thank you! Feedback saved successfully."


def show_feedback():
    feedbacks = load_feedbacks()
    if not feedbacks:
        return "Abhi tak koi feedback nahi mila. Pehla feedback do! ⭐"

    html = "<h4 style='color:#00cc00;'>All Feedbacks</h4><hr>"
    for fb in reversed(feedbacks):
        html += f"""
        <div style="border-left:5px solid #00cc00; padding:15px; margin:12px 0; 
                    background:#f8f9fa; border-radius:8px;">
            <div style="font-size:24px;">{fb['rating']}</div>
            <strong>Name:</strong> {fb['name']}<br>
            <strong>Feedback:</strong> {fb['feedback']}
        </div>
        """
    return html

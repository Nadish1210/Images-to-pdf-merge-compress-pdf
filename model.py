import os
import tempfile
import json
from PIL import Image
import fitz  # PyMuPDF for compression
from PyPDF2 import PdfMerger

# ReportLab imports for better PDF creation with orientation

# ReportLab imports
from reportlab.lib.pagesizes import A4, letter, legal
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

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
            pil_img = Image.open(uploaded_file).convert("RGB")
            img_width, img_height = pil_img.size
            img_reader = ImageReader(uploaded_file)

            if page_size == "Original":
                page_w = img_width
                page_h = img_height
                draw_w = img_width
                draw_h = img_height
                x = 0
                y = 0
            else:
                base_size = PAGE_SIZES[page_size]
                
                # === Landscape Fix ===
                if orientation.lower() == "landscape":
                    page_size_tuple = landscape(base_size)
                else:
                    page_size_tuple = portrait(base_size)

                page_w, page_h = page_size_tuple

                # Scale image to fit page properly
                scale = min(page_w / img_width, page_h / img_height) * 0.97   # 3% margin
                draw_w = img_width * scale
                draw_h = img_height * scale

                # Center image
                x = (page_w - draw_w) / 2
                y = (page_h - draw_h) / 2

            # Set page size for this page
            c.setPageSize((page_w, page_h))
            
            # Draw image
            c.drawImage(img_reader, x, y, width=draw_w, height=draw_h,
                        preserveAspectRatio=True, anchor='c')

            c.showPage()   # Important: next page

        c.save()

        # Read bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        os.unlink(pdf_path)

        return pdf_bytes, f"✅ {len(uploaded_files)} images converted! (Landscape Fixed)"

    except Exception as e:
        return None, f"Error: {str(e)}"


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
    """Feedbacks ko load karo"""
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_feedbacks(feedbacks):
    """Feedbacks ko save karo"""
    try:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(feedbacks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Feedback save karne mein problem hui: {e}")
        return False


def save_feedback(name: str, feedback_text: str, rating: str):
    """User ka feedback save karne ka function"""
    
    if not feedback_text or not feedback_text.strip():
        return "❌ Feedback likhna zaroori hai!"

    if not rating:
        return "❌ Rating select karna zaroori hai!"

    feedbacks = load_feedbacks()

    new_feedback = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name.strip() if name and name.strip() else "Anonymous",
        "feedback": feedback_text.strip(),
        "rating": rating
    }

    feedbacks.append(new_feedback)
    
    if save_feedbacks(feedbacks):
        return "✅ Thank you! Feedback saved successfully. ⭐"
    else:
        return "❌ Feedback save nahi ho saka. Baad mein try karein."


def show_feedback():
    """Sab feedbacks ko beautiful tarike se show karo"""
    feedbacks = load_feedbacks()
    
    if not feedbacks:
        return "Abhi tak koi feedback nahi mila. Pehla feedback do! ⭐"

    html = "<h4 style='color:#00cc00; text-align:center;'>📋 All User Feedbacks</h4><hr style='border-color:#00cc00;'>"

    for fb in reversed(feedbacks):   # Latest feedback sabse upar
        html += f"""
        <div style="border-left: 6px solid #00cc00; 
                    padding: 15px; 
                    margin: 12px 0; 
                    background: #f8f9fa; 
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 28px; margin-bottom: 8px;">{fb['rating']}</div>
            <strong>Name:</strong> {fb['name']}<br>
            <strong>Time:</strong> {fb['timestamp']}<br>
            <strong>Feedback:</strong> {fb['feedback']}
        </div>
        """
    
    return html

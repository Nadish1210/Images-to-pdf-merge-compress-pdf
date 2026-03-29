import os
import tempfile
import io
from PIL import Image
import numpy as np
# Agar aap cv2 use kar rahe ho to uncomment kar do
# import cv2

# Compression map (agar aapke purane code mein tha)
compression_map = {
    "Balanced (Good Quality + Small Size)": 0.7,
    "High Compression": 0.5,
    "Maximum Compression": 0.3,
    "Best Quality": 0.95
}

def images_to_pdf(uploaded_files, page_size="A4", orientation="Portrait", quality="High", enable_compression=True):
    """Convert multiple uploaded images to PDF"""
    if not uploaded_files:
        return None, "Koi image upload nahi ki gayi!"

    try:
        pil_images = []
        for uploaded_file in uploaded_files:
            # Convert UploadedFile to PIL Image
            image = Image.open(uploaded_file).convert("RGB")
            pil_images.append(image)

        if not pil_images:
            return None, "Images load nahi ho saki!"

        # Quality mapping
        quality_map = {"Low": 60, "Medium": 75, "High": 85, "Maximum": 95}
        save_quality = quality_map.get(quality, 85)

        # Create temporary PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            pdf_path = tmp.name

        # Save as PDF (first image + append rest)
        pil_images[0].save(
            pdf_path,
            save_all=True,
            append_images=pil_images[1:],
            quality=save_quality,
            optimize=enable_compression,
            dpi=(300, 300) if quality == "Maximum" else (200, 200)
        )

        # Read bytes for download
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # Cleanup
        os.unlink(pdf_path)

        return pdf_bytes, f"✅ {len(uploaded_files)} images successfully PDF mein convert ho gayi!"

    except Exception as e:
        return None, f"Conversion error: {str(e)}"


def merge_pdfs(uploaded_pdfs):
    """Merge multiple uploaded PDF files"""
    if len(uploaded_pdfs) < 2:
        return None, "Merge karne ke liye kam se kam 2 PDFs upload karein!"

    try:
        from PyPDF2 import PdfMerger   # ya pypdf2 use karo

        merger = PdfMerger()
        temp_paths = []

        for pdf_file in uploaded_pdfs:
            # Save to temp file
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
        for path in temp_paths:
            if os.path.exists(path):
                os.unlink(path)

        return merged_bytes, f"✅ {len(uploaded_pdfs)} PDFs successfully merge ho gaye!"

    except Exception as e:
        return None, f"Merge error: {str(e)}"


def compress_pdf(uploaded_pdf, compression_level="Balanced (Good Quality + Small Size)"):
    """Compress uploaded PDF"""
    if not uploaded_pdf:
        return None, "PDF upload karein!", ""

    try:
        # Simple compression using PyMuPDF (fitz) - better for cloud
        import fitz  # PyMuPDF

        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_pdf.getvalue())
            input_path = tmp.name

        doc = fitz.open(input_path)
        output_path = input_path.replace(".pdf", "_compressed.pdf")

        # Basic compression
        for page in doc:
            page.clean_contents()

        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

        with open(output_path, "rb") as f:
            compressed_bytes = f.read()

        # Cleanup
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)   # agar bytes le liye to delete

        table_md = "### Compression Complete\nOriginal size vs Compressed size show karne ke liye advanced logic add kar sakte hain."

        return compressed_bytes, "✅ PDF successfully compressed!", table_md

    except Exception as e:
        return None, f"Compression error: {str(e)}", ""


# ====================== Feedback Functions ======================
feedbacks = []

def save_feedback(name, feedback_text, rating):
    if not feedback_text or not feedback_text.strip():
        return "❌ Feedback likhna zaroori hai!"
    
    feedbacks.append({
        "name": name.strip() if name and name.strip() else "Anonymous",
        "feedback": feedback_text.strip(),
        "rating": rating
    })
    return "✅ Thank you! Feedback successfully save ho gaya."


def show_feedback():
    if not feedbacks:
        return "Abhi tak koi feedback nahi mila. Pehla feedback do! ⭐"

    html = """
    <h4 style="color:#00cc00;">All Feedbacks from Users</h4>
    <hr style="border-color:#00cc00;">
    """
    
    for fb in reversed(feedbacks):  # Latest feedback pehle
        html += f"""
        <div style="border-left: 5px solid #00cc00; 
                    padding: 15px; 
                    margin: 15px 0; 
                    background-color: #f8f9fa; 
                    border-radius: 8px;">
            <div style="font-size: 24px; margin-bottom: 8px;">{fb['rating']}</div>
            <strong>Name:</strong> {fb['name']}<br>
            <strong>Feedback:</strong> {fb['feedback']}
        </div>
        """
    
    return html

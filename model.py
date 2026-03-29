# model.py
from PIL import Image, ImageEnhance
import tempfile
import os
import cv2
import numpy as np
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import csv
import subprocess
import shutil
import pandas as pd
from typing import List, Tuple

# ---------------- IMAGE ENHANCEMENT & SCALING ---------------- #
def enhance_image(image: Image.Image, quality_level: str) -> Image.Image:
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    quality_map = {
        "Low": (1.0, 1.0),
        "Medium": (1.1, 1.05),
        "High": (1.25, 1.1),
        "Maximum": (1.4, 1.2)
    }
    sharp, contrast = quality_map.get(quality_level, (1.2, 1.1))
    
    image = ImageEnhance.Sharpness(image).enhance(sharp)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    return image

def compress_with_opencv(pil_img, quality=40):
    img = np.array(pil_img)[:, :, ::-1]  # PIL → BGR
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, enc = cv2.imencode('.jpg', img, encode_param)
    dec = cv2.imdecode(enc, cv2.IMREAD_COLOR)
    return Image.fromarray(cv2.cvtColor(dec, cv2.COLOR_BGR2RGB))

# ---------------- IMAGE → PDF ---------------- #
def images_to_pdf(images, page_size: str, orientation: str, quality_level: str, compression: bool = True):
    if not images:
        return None, "⚠️ Please upload at least one image."
    
    page_sizes = {
        "A4": (2480, 3508),
        "Letter": (2550, 3300),
        "Legal": (2550, 4200),
        "Original": None
    }
    
    processed = []
    target_size = page_sizes.get(page_size)
    
    for img_file in images:
        if isinstance(img_file, str):
            img = Image.open(img_file)
        else:
            img = Image.open(img_file.name) if hasattr(img_file, 'name') else img_file
        
        img = enhance_image(img, quality_level)
        
        if target_size:
            if orientation == "Landscape":
                target_size = (target_size[1], target_size[0])
            
            bg = Image.new("RGB", target_size, (255, 255, 255))
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            offset = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)
            bg.paste(img, offset)
            img = bg
        
        if compression:
            img = compress_with_opencv(img, quality=40)
        
        processed.append(img)
    
    output_path = os.path.join(tempfile.gettempdir(), "Nadish_Converted_File.pdf")
    processed[0].save(output_path, "PDF", save_all=True, append_images=processed[1:], resolution=100)
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    return output_path, f"✅ PDF Created | Size: {size_mb:.2f} MB"

# ---------------- PDF MERGE ---------------- #
def merge_pdfs(pdf_files):
    if not pdf_files:
        return None, "⚠️ Please upload PDFs."
    
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf.name if hasattr(pdf, 'name') else pdf)
    
    output_path = os.path.join(tempfile.gettempdir(), "Nadish_Merged_File.pdf")
    merger.write(output_path)
    merger.close()
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    return output_path, f"✅ Merged {len(pdf_files)} PDFs | Size: {size_mb:.2f} MB"

# ---------------- PDF COMPRESSION ---------------- #
compression_map = {
    "Maximum Compression (Smallest Size)": "screen",
    "Balanced (Good Quality + Small Size)": "ebook",
    "High Quality (Larger Size)": "printer",
    "Original Quality (Least Compression)": "prepress"
}

def compress_pdf(pdf_file, compression_level: str):
    if not pdf_file:
        return None, "⚠️ Upload a PDF.", None
    
    gs_level = compression_map[compression_level]
    
    original_copy = os.path.join(tempfile.gettempdir(), "Nadish_Original.pdf")
    shutil.copy(pdf_file.name if hasattr(pdf_file, 'name') else pdf_file, original_copy)
    
    output_path = os.path.join(tempfile.gettempdir(), f"Nadish_Compressed_{gs_level}.pdf")
    
    original_size = os.path.getsize(original_copy) / (1024 * 1024)
    
    gs_command = [
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{gs_level}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        f"-sOutputFile={output_path}", original_copy
    ]
    
    try:
        subprocess.run(gs_command, check=True, capture_output=True)
        new_size = os.path.getsize(output_path) / (1024 * 1024)
        reduction = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0
        
        table = f"""
| Metric                | Value          |
|-----------------------|----------------|
| Original Size (MB)    | {original_size:.2f} |
| Compressed Size (MB)  | {new_size:.2f}     |
| Reduction (%)         | {reduction:.1f}%   |
"""
        return output_path, f"✅ Compression Successful!", table
    except Exception as e:
        return None, f"❌ Ghostscript Error: {str(e)}", None

# ---------------- FEEDBACK ---------------- #
def save_feedback(name_or_email: str, feedback_text: str, rating: str):
    if not rating:
        return "⚠️ Please select a rating."
    
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.csv")
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Feedback", "Rating"])
        writer.writerow([name_or_email or "Anonymous", feedback_text or "N/A", rating])
    
    return "✅ Feedback saved! Thank you."

def show_feedback():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.csv")
    if not os.path.isfile(file_path):
        return "⚠️ No feedback yet."
    
    df = pd.read_csv(file_path)
    return df.to_markdown(index=False)
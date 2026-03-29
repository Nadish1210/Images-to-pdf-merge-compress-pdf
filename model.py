import streamlit as st
from model import (
    images_to_pdf,
    merge_pdfs,
    compress_pdf,
    save_feedback,
    show_feedback
)

# Page Configuration
st.set_page_config(
    page_title="Its Nadish - Image to PDF",
    page_icon="🖼️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        color: #00cc00;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
    }
    .download-btn {
        background-color: #00cc00 !important;
        color: white !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Its Nadish</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powerful Image to PDF | Merge | Compress Tool</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🖼️ Images to PDF", "📑 Merge PDFs", "📉 Compress PDF"])

# ====================== Tab 1: Images to PDF ======================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img_files = st.file_uploader(
            "Upload Images (JPG, PNG, WEBP, etc.)",
            type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
            accept_multiple_files=True
        )
    
    with col2:
        p_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "Original"], index=0)
        p_orient = st.radio("Orientation", ["Portrait", "Landscape"], horizontal=True)
        p_qual = st.selectbox("Quality", ["Low", "Medium", "High", "Maximum"], index=2)
        p_comp = st.checkbox("Enable Compression", value=True)
    
    if st.button("Convert to PDF", type="primary", use_container_width=True):
        if not img_files:
            st.error("Please upload at least one image!")
        else:
            with st.spinner("Converting images to PDF..."):
                download_bytes, message = images_to_pdf(
                    img_files, p_size, p_orient, p_qual, p_comp
                )
                if download_bytes:
                    st.success(message)
                    st.download_button(
                        label="📥 Download PDF",
                        data=download_bytes,
                        file_name="images_to_pdf_by_Nadish.pdf",   # ← Yeh change kiya
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                else:
                    st.error(message)

# ====================== Tab 2: Merge PDFs ======================
with tab2:
    merge_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if st.button("Merge Files", type="primary", use_container_width=True):
        if len(merge_files) < 2:
            st.warning("Please upload at least 2 PDF files!")
        else:
            with st.spinner("Merging PDFs..."):
                download_bytes, message = merge_pdfs(merge_files)
                if download_bytes:
                    st.success(message)
                    st.download_button(
                        label="📥 Download Merged PDF",
                        data=download_bytes,
                        file_name="merged_by_Nadish.pdf",      # ← Yeh change kiya
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                else:
                    st.error(message)

# ====================== Tab 3: Compress PDF ======================
with tab3:
    comp_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    comp_lvl = st.selectbox(
        "Compression Level",
        ["Balanced (Good Quality + Small Size)", 
         "High Compression", 
         "Maximum Compression", 
         "Best Quality"]
    )
    
    if st.button("Compress Now", type="primary", use_container_width=True):
        if not comp_file:
            st.error("Please upload a PDF file!")
        else:
            with st.spinner("Compressing PDF..."):
                download_bytes, message, _ = compress_pdf(comp_file, comp_lvl)
                if download_bytes:
                    st.success(message)
                    st.download_button(
                        label="📥 Download Compressed PDF",
                        data=download_bytes,
                        file_name="compressed_by_Nadish.pdf",   # ← Yeh change kiya
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                else:
                    st.error(message)

# ====================== Feedback Section ======================
with st.expander("⭐ Give Feedback to Nadish", expanded=False):
    f_name = st.text_input("Name or Email (Optional)")
    f_txt = st.text_area("Your Feedback", height=100)
    f_rate = st.radio("Rating", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], horizontal=True)
    
    if st.button("Submit Feedback", type="primary"):
        if f_txt.strip():
            msg = save_feedback(f_name, f_txt, f_rate)
            st.success(msg)
        else:
            st.warning("Please write some feedback!")

with st.expander("📋 View All Feedback", expanded=False):
    if st.button("Show All Feedback", type="primary"):
        html = show_feedback()
        st.markdown(html, unsafe_allow_html=True)

# Reset Button
if st.button("🔄 Reset Everything", type="secondary"):
    st.rerun()

st.caption("Made with ❤️ by Nadish")        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
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

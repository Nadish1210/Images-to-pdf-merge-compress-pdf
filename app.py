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

st.caption("Made with ❤️ by Nadish")        color: white !important;
        font-weight: bold;
    }
    .reset-btn {
        background-color: #ff4444 !important;
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
            "Upload Images (JPG, PNG, etc.)",
            type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
            accept_multiple_files=True,
            help="Multiple images select kar sakte ho"
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
                try:
                    download_bytes, message = images_to_pdf(
                        img_files, p_size, p_orient, p_qual, p_comp
                    )
                    if download_bytes:
                        st.success(message)
                        st.download_button(
                            label="📥 Download PDF",
                            data=download_bytes,
                            file_name="converted.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ====================== Tab 2: Merge PDFs ======================
with tab2:
    merge_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if st.button("Merge Files", type="primary", use_container_width=True):
        if len(merge_files) < 2:
            st.warning("Please upload at least 2 PDF files to merge!")
        else:
            with st.spinner("Merging PDFs..."):
                try:
                    download_bytes, message = merge_pdfs(merge_files)
                    if download_bytes:
                        st.success(message)
                        st.download_button(
                            label="📥 Download Merged PDF",
                            data=download_bytes,
                            file_name="merged.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ====================== Tab 3: Compress PDF ======================
with tab3:
    comp_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    # compression_map model.py mein hai, isliye assume kar rahe hain
    comp_lvl = st.selectbox(
        "Compression Level",
        list(compression_map.keys()) if 'compression_map' in globals() else [
            "Balanced (Good Quality + Small Size)",
            "High Compression",
            "Maximum Compression",
            "Best Quality"
        ],
        index=0
    )
    
    if st.button("Compress Now", type="primary", use_container_width=True):
        if not comp_file:
            st.error("Please upload a PDF file!")
        else:
            with st.spinner("Compressing PDF..."):
                try:
                    download_bytes, message, table_md = compress_pdf(comp_file, comp_lvl)
                    if download_bytes:
                        st.success(message)
                        if table_md:
                            st.markdown(table_md)
                        st.download_button(
                            label="📥 Download Compressed PDF",
                            data=download_bytes,
                            file_name="compressed.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ====================== Feedback Section ======================
with st.expander("⭐ Give Feedback to Nadish", expanded=False):
    f_name = st.text_input("Name or Email (Optional)")
    f_txt = st.text_area("Your Feedback", height=100)
    f_rate = st.radio("Rating", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], horizontal=True)
    
    if st.button("Submit Feedback", type="primary"):
        if f_txt.strip():
            with st.spinner("Saving feedback..."):
                msg = save_feedback(f_name, f_txt, f_rate)
                st.success(msg)
        else:
            st.warning("Please write some feedback!")

with st.expander("📋 View All Feedback", expanded=False):
    if st.button("Show All Feedback"):
        feedbacks = show_feedback()
        st.markdown(feedbacks)

# Reset Button
if st.button("🔄 Reset Everything", type="secondary"):
    st.rerun()   # Streamlit mein simple rerun best hota hai

st.caption("Made with ❤️ by Nadish")

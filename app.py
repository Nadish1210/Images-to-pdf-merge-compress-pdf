import streamlit as st
from model import (
    images_to_pdf, 
    merge_pdfs, 
    compress_pdf, 
    save_feedback, 
    show_feedback
)

# Initialize session state for reset
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

st.set_page_config(
    page_title="Its Nadish - Image to PDF",
    page_icon="🖼️",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {color: #00cc00; font-size: 42px; font-weight: bold; text-align: center; margin-bottom: 10px;}
    .sub-title {text-align: center; color: #666; margin-bottom: 30px;}
    .stButton>button {width: 100%;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Its Nadish</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powerful Image to PDF | Merge | Compress Tool</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🖼️ Images to PDF", "📑 Merge PDFs", "📉 Compress PDF"])

# Tab 1: Images to PDF
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        img_files = st.file_uploader(
            "Upload Images", 
            type=["jpg","jpeg","png","webp","bmp","tiff"], 
            accept_multiple_files=True,
            key=f"img_uploader_{st.session_state.reset_key}"
        )
    with col2:
        p_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "Original"])
        p_orient = st.radio("Orientation", ["Portrait", "Landscape"], horizontal=True)
        p_qual = st.selectbox("Quality", ["Low", "Medium", "High", "Maximum"], index=2)
        p_comp = st.checkbox("Enable Compression", value=True)

    if st.button("Convert to PDF", type="primary", use_container_width=True):
        if not img_files:
            st.error("At least one image upload karein!")
        else:
            with st.spinner("Converting..."):
                bytes_data, msg = images_to_pdf(img_files, p_size, p_orient, p_qual, p_comp)
                if bytes_data:
                    st.success(msg)
                    st.download_button("📥 Download PDF", bytes_data, "images_to_pdf_by_Nadish.pdf", "application/pdf")
                else:
                    st.error(msg)

# Tab 2: Merge PDFs
with tab2:
    merge_files = st.file_uploader(
        "Upload PDF Files", 
        type=["pdf"], 
        accept_multiple_files=True,
        key=f"merge_uploader_{st.session_state.reset_key}"
    )
    if st.button("Merge Files", type="primary", use_container_width=True):
        if len(merge_files) < 2:
            st.warning("At least 2 PDFs upload karein!")
        else:
            with st.spinner("Merging..."):
                bytes_data, msg = merge_pdfs(merge_files)
                if bytes_data:
                    st.success(msg)
                    st.download_button("📥 Download Merged PDF", bytes_data, "merged_by_Nadish.pdf", "application/pdf")
                else:
                    st.error(msg)

# Tab 3: Compress PDF
with tab3:
    comp_file = st.file_uploader(
        "Upload PDF", 
        type=["pdf"],
        key=f"comp_uploader_{st.session_state.reset_key}"
    )
    comp_lvl = st.selectbox("Compression Level", 
        ["Balanced (Good Quality + Small Size)", "High Compression", "Maximum Compression", "Best Quality"])
    
    if st.button("Compress Now", type="primary", use_container_width=True):
        if not comp_file:
            st.error("PDF upload karein!")
        else:
            with st.spinner("Compressing..."):
                bytes_data, msg, _ = compress_pdf(comp_file, comp_lvl)
                if bytes_data:
                    st.success(msg)
                    st.download_button("📥 Download Compressed PDF", bytes_data, "compressed_by_Nadish.pdf", "application/pdf")
                else:
                    st.error(msg)

# Feedback Section
with st.expander("⭐ Give Feedback to Nadish", expanded=False):
    f_name = st.text_input("Name or Email (Optional)")
    f_txt = st.text_area("Your Feedback", height=100)
    f_rate = st.radio("Rating", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"], horizontal=True)
    if st.button("Submit Feedback", type="primary"):
        if f_txt.strip():
            st.success(save_feedback(f_name, f_txt, f_rate))
        else:
            st.warning("Feedback likhna zaroori hai!")

with st.expander("📋 View All Feedback", expanded=False):
    if st.button("Show All Feedback", type="primary"):
        st.markdown(show_feedback(), unsafe_allow_html=True)

# ==================== Reset Button ====================
if st.button("🔄 Reset Everything", type="secondary"):
    st.session_state.reset_key += 1
    st.rerun()

st.caption("Made with ❤️ by Nadish")

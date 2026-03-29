import streamlit as st
from model import (
    images_to_pdf,
    merge_pdfs,
    compress_pdf,
    save_feedback,
    show_feedback
)

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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Its Nadish</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powerful Image to PDF | Merge | Compress Tool</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🖼️ Images to PDF", "📑 Merge PDFs", "📉 Compress PDF"])

# ====================== Images to PDF ======================
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        img_files = st.file_uploader("Upload Images", type=["jpg","jpeg","png","webp","bmp","tiff"], accept_multiple_files=True)
    with col2:
        p_size = st.selectbox("Page Size", ["A4", "Letter", "Legal", "Original"])
        p_orient = st.radio("Orientation", ["Portrait", "Landscape"], horizontal=True)
        p_qual = st.selectbox("Quality", ["Low", "Medium", "High", "Maximum"], index=2)
        p_comp = st.checkbox("Enable Compression", value=True)

    if st.button("Convert to PDF", type="primary", use_container_width=True):
        if img_files:
            with st.spinner("Converting..."):
                bytes_data, msg = images_to_pdf(img_files, p_size, p_orient, p_qual, p_comp)
                if bytes_data:
                    st.success(msg)
                    st.download_button("📥 Download PDF", bytes_data, "images_to_pdf_by_Nadish.pdf", "application/pdf")
                else:
                    st.error(msg)

# ====================== Merge PDFs ======================
with tab2:
    merge_files = st.file_uploader("Upload PDF Files", type=["pdf"], accept_multiple_files=True)
    if st.button("Merge Files", type="primary", use_container_width=True):
        if len(merge_files) >= 2:
            with st.spinner("Merging..."):
                bytes_data, msg = merge_pdfs(merge_files)
                if bytes_data:
                    st.success(msg)
                    st.download_button("📥 Download Merged PDF", bytes_data, "merged_by_Nadish.pdf", "application/pdf")
                else:
                    st.error(msg)

# ====================== Compress PDF ======================
with tab3:
    comp_file = st.file_uploader("Upload PDF", type=["pdf"])
    comp_lvl = st.selectbox("Compression Level", ["Balanced (Good Quality + Small Size)", "High Compression", "Maximum Compression", "Best Quality"])
    
    if st.button("Compress Now", type="primary", use_container_width=True):
        if comp_file:
            with st.spinner("Compressing..."):
                bytes_data, msg, _ = compress_pdf(comp_file, comp_lvl)
                if bytes_data:
                    st.success(msg)
                    st.download_button("📥 Download Compressed PDF", bytes_data, "compressed_by_Nadish.pdf", "application/pdf")
                else:
                    st.error(msg)

# Feedback
with st.expander("⭐ Give Feedback to Nadish"):
    name = st.text_input("Name or Email (Optional)")
    feedback = st.text_area("Your Feedback")
    rating = st.radio("Rating", ["⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"], horizontal=True)
    if st.button("Submit Feedback"):
        if feedback.strip():
            st.success(save_feedback(name, feedback, rating))
        else:
            st.warning("Feedback likho!")

with st.expander("📋 View All Feedback"):
    if st.button("Show Feedback"):
        st.markdown(show_feedback(), unsafe_allow_html=True)

if st.button("Reset Everything"):
    st.rerun()

st.caption("Made with ❤️ by Nadish")

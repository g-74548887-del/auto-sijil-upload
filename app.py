import streamlit as st
from docxtpl import DocxTemplate
import io
import zipfile
import pandas as pd
import os

st.set_page_config(page_title="Auto Jana Sijil", page_icon="🎓")

st.title("🎓 Sistem Jana Sijil Sekolah")
st.write("Muat naik fail CSV (nama, ic) untuk jana sijil automatik")

# Nama fail template (gunakan .docx.docx seperti yang cikgu mahu)
TEMPLATE_FILE = "template_sijil.docx.docx"

# Semak template ada
if not os.path.exists(TEMPLATE_FILE):
    st.error(f"⚠️ Fail '{TEMPLATE_FILE}' tidak dijumpai di repo!")
    st.stop()

# Muat naik CSV
uploaded_file = st.file_uploader("Muat naik fail CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Semak kolum ada
        if "nama" not in df.columns or "ic" not in df.columns:
            st.error("CSV mesti ada kolum 'nama' dan 'ic'")
            st.stop()

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zipf:
            for index, row in df.iterrows():
                nama = row["nama"]
                ic = row["ic"]

                doc = DocxTemplate(TEMPLATE_FILE)
                context = {"nama": nama, "ic": ic}
                doc.render(context)

                # Simpan ke buffer dan masukkan dalam ZIP
                output = io.BytesIO()
                doc.save(output)
                zipf.writestr(f"SIJIL_{nama}.docx", output.getvalue())

        zip_buffer.seek(0)
        st.download_button(
            label="📥 Muat Turun Semua Sijil (ZIP)",
            data=zip_buffer,
            file_name="sijil.zip",
            mime="application/zip"
        )
    except Exception as e:
        st.error(f"Ralat semasa jana sijil: {e}")

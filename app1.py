import streamlit as st
from docxtpl import DocxTemplate
import io
import zipfile
import pandas as pd

st.set_page_config(page_title="Auto Jana Sijil Sekolah", page_icon="🎓")

st.title("🎓 Sistem Jana Sijil Automatik Sekolah")
st.write("Muat naik fail **template .docx** dan **fail CSV (nama, ic)** untuk jana sijil automatik.")

# 1️⃣ Muat naik template DOCX
template_file = st.file_uploader("📄 Muat naik template sijil (.docx)", type=["docx"])

# 2️⃣ Muat naik CSV
csv_file = st.file_uploader("📑 Muat naik fail CSV (nama, ic)", type=["csv"])

if template_file and csv_file:
    try:
        df = pd.read_csv(csv_file)

        # Semak kolum wajib
        if "nama" not in df.columns or "ic" not in df.columns:
            st.error("⚠️ Fail CSV mesti ada kolum 'nama' dan 'ic'")
            st.stop()

        # Guna template Word yang diupload
        template_bytes = template_file.read()
        zip_buffer = io.BytesIO()

        # Jana sijil dan zip semua
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zipf:
            for index, row in df.iterrows():
                nama = row["nama"]
                ic = row["ic"]

                doc = DocxTemplate(io.BytesIO(template_bytes))
                context = {"nama": nama, "ic": ic}
                doc.render(context)

                output = io.BytesIO()
                doc.save(output)
                zipf.writestr(f"Sijil_{nama}.docx", output.getvalue())

        zip_buffer.seek(0)

        # Butang muat turun ZIP
        st.success("✅ Semua sijil berjaya dijana!")
        st.download_button(
            label="📥 Muat Turun Semua Sijil (ZIP)",
            data=zip_buffer,
            file_name="sijil_automatik.zip",
            mime="application/zip"
        )

    except Exception as e:
        st.error(f"❌ Ralat semasa menjana sijil: {e}")

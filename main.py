import os
import requests
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import dashscope
from dashscope import Generation  

# Load API key dari .env
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY tidak ditemukan di .env!")

# Set API key ke dashscope
dashscope.api_key = api_key

# Inisialisasi saldo e-wallet
if "saldo_ewallet" not in st.session_state:
    st.session_state.saldo_ewallet = 0

# Streamlit UI
st.title("Sampah Bercuan")
st.write("Upload gambar sampah")

# Layout utama
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hasil Upload Gambar")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Gambar yang diupload", use_container_width=True)
        img_path = f"temp_{uploaded_file.name}"
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        img_path = None
        st.write("Belum ada gambar diupload.")

with col2:
    st.subheader("Chatbot - Tanya Manfaat Sampah")
    chat_input = st.text_input("Tanyakan sesuatu tentang sampah:")
    chat_response = ""
    if chat_input:
        chat_response = Generation.call(
            model="qwen-max",
            messages=[{"role": "user", "content": chat_input}]
        )
        if chat_response and "output" in chat_response:
            chat_response = chat_response["output"]["text"]
        else:
            chat_response = "Tidak ada jawaban."
    st.text_area("Jawaban Chatbot:", chat_response, height=150)

st.markdown("---")

# Fungsi untuk klasifikasi gambar
def categorize_image(file_path):
    try:
        response = Generation.call(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Apa kategori dari gambar ini?"},
                        {"type": "image_url", "image_url": {"url": file_path}},
                    ],
                }
            ],
        )
        if response and "output" in response:
            return response["output"]["text"]
        return "Gagal mendapatkan kategori."
    except Exception as e:
        return f"Error: {str(e)}"

# Jika gambar diupload, proses klasifikasi
if img_path:
    category = categorize_image(img_path)
    st.write(f"Kategori Sampah: {category}")
    
    # Jika kategori sampah adalah plastik, tambahkan saldo e-wallet
    if "plastik" in category.lower():
        tambahan_saldo = 50 * (5000 / 1000)  # 50 gram x harga plastik 5000/kg
        st.session_state.saldo_ewallet += tambahan_saldo
        st.write(f"Anda mendapatkan saldo e-wallet sebesar Rp {tambahan_saldo:.2f}")

st.markdown("---")
st.write("tes")

# Tampilkan saldo e-wallet
st.subheader("E-Wallet")
st.write(f"Saldo Anda: Rp {st.session_state.saldo_ewallet:.2f}")

st.markdown("---")

# Opsi penggunaan saldo
st.subheader("Gunakan Saldo Anda")
def gunakan_saldo(jumlah, tujuan):
    if st.session_state.saldo_ewallet >= jumlah:
        st.session_state.saldo_ewallet -= jumlah
        st.success(f"Berhasil menggunakan Rp {jumlah:.2f} untuk {tujuan}")
    else:
        st.error("Saldo tidak mencukupi!")

st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    if st.button("Gunakan untuk Investasi (Rp 5000)"):
        gunakan_saldo(5000, "Investasi")

with col4:
    st.subheader("Chatbot - Asistant Investadi Anda")
    chat_input = st.text_input("Sudahkan anda menabung enmas hari ini?")
    chat_response = ""
    if chat_input:
        chat_response = Generation.call(
            model="qwen-max",
            messages=[{"role": "user", "content": chat_input}]
        )
        if chat_response and "output" in chat_response:
            chat_response = chat_response["output"]["text"]
        else:
            chat_response = "Tidak ada jawaban."
   # st.text_area("Jawaban Chatbot:", chat_response, height=150)

# with col4:
#     if st.button("Gunakan untuk Beli Emas (Rp 10000)"):
#         gunakan_saldo(10000, "Beli Emas")


st.markdown("---")

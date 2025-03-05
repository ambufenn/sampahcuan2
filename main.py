import os
import requests
import streamlit as st
import dashscope
from dotenv import load_dotenv
from dashscope import Generation
from dashscope import Application

# Folder untuk menyimpan gambar yang di-upload
UPLOAD_FOLDER = "upload"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set base URL API Alibaba
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

# Load API key dari .env
load_dotenv()
api_key = os.getenv("API_KEY")
app_id = os.getenv("ID_APP")

# Cek jika API key tersedia
if not api_key:
    raise ValueError("API_KEY tidak ditemukan di .env!")

# Set API key ke dashscope
dashscope.api_key = api_key

# Inisialisasi saldo e-wallet di session state jika belum ada
if "saldo_ewallet" not in st.session_state:
    st.session_state.saldo_ewallet = 0

# Streamlit UI
st.title("Sampah Bercuan")
st.write("Upload gambar sampah untuk klasifikasi dan mendapatkan saldo e-wallet.")

# Layout utama untuk upload gambar
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

st.markdown("---")


# Fungsi untuk klasifikasi gambar menggunakan API
def categorize_image(file_path):
    try:
        with open(file_path, "rb") as img_file:
            img_data = img_file.read()  # Membaca file gambar dalam format bytes

        # Memanggil API Alibaba untuk menganalisis gambar
        response = Application.call(
            app_id = app_id,
            app_key = api_key,
            prompt= "Apa kategori dari gambar ini?",
            file = img_data,
        )

        # Cek apakah response berhasil dan memiliki output
        if response and "output" in response:
            return response["output"]["text"]
        else:
            return "Kategori tidak ditemukan."
    except Exception as e:
        return f"Error: {str(e)}"


# Menampilkan hasil upload gambar dan klasifikasi
col1, col2 = st.columns(2)

# Kolom 1: Menampilkan gambar yang diupload
with col1:
    st.subheader("Hasil Upload Gambar")
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Menampilkan gambar di aplikasi
        st.image(file_path, caption="Gambar yang diupload", use_container_width=True)

        # Membuat URL yang bisa diakses di dalam aplikasi
        img_path = f"https://raw.githubusercontent.com/ambufenn/sampahcuan2/alibaba-root/{UPLOAD_FOLDER}/{uploaded_file.name}"
        #
        # st.image(uploaded_file, caption="Gambar yang diupload", use_container_width=True)
        # img_path = f"temp_{uploaded_file.name}"
        # with open(img_path, "wb") as f:
        #     f.write(uploaded_file.getbuffer())
    else:
        img_path = None
        st.write("Belum ada gambar diupload.")

# Kolom 2: Chatbot Tanya Manfaat Sampah
with col2:
    st.subheader("Chatbot - Tanya Manfaat Sampah")
    chat_input = st.text_input("Tanyakan sesuatu tentang sampah:")
    chat_response = ""
    if chat_input:
        chat_response = Application.call(
            app_id=app_id,
            app_key=api_key,
            prompt="Bantu saya menjelaskan tentang "+chat_input,
        )
        if chat_response and "output" in chat_response:
            chat_response = chat_response["output"]["text"]
        else:
            chat_response = "Tidak ada jawaban."
    st.text_area("Jawaban Chatbot:", chat_response, height=150)

st.markdown("---")

# Jika gambar diupload, proses klasifikasi dan tampilkan kategori
if img_path:
    category = categorize_image(img_path)
    st.write(f"Kategori Sampah: {category}")

    # Jika kategori adalah plastik, tambahkan saldo e-wallet
    if "plastik" in category.lower():
        tambahan_saldo = 50 * (5000 / 1000)  # 50 gram x harga plastik 5000/kg
        st.session_state.saldo_ewallet += tambahan_saldo
        st.write(f"Anda mendapatkan saldo e-wallet sebesar Rp {tambahan_saldo:.2f}")

# Tampilkan saldo e-wallet
st.markdown("---")
st.subheader("E-Wallet")
st.write(f"Saldo Anda: Rp {st.session_state.saldo_ewallet:.2f}")

st.markdown("---")


# Fungsi untuk menggunakan saldo e-wallet
def gunakan_saldo(jumlah, tujuan):
    if st.session_state.saldo_ewallet >= jumlah:
        st.session_state.saldo_ewallet -= jumlah
        st.success(f"Berhasil menggunakan Rp {jumlah:.2f} untuk {tujuan}")
    else:
        st.error("Saldo tidak mencukupi!")

# Layout untuk penggunaan saldo
st.subheader("Gunakan Saldo Anda")
col3, col4 = st.columns(2)

# Kolom 1: Tombol untuk menggunakan saldo untuk investasi
with col3:
    if st.button("Gunakan untuk Investasi (Rp 5000)"):
        gunakan_saldo(5000, "Investasi")

# Kolom 2: Chatbot - Asisten Investasi Anda
with col4:
    st.subheader("Chatbot - Asisten Investasi Anda")
    chat_input = st.text_input("Sudahkah Anda menabung emas hari ini?")
    chat_response = ""
    if chat_input:
        chat_response = Application.call(
            app_id=app_id,
            app_key=api_key,
            prompt="Bantu saya menjelaskan investasi dari "+chat_input,
        )
        if chat_response and "output" in chat_response:
            chat_response = chat_response["output"]["text"]
        else:
            chat_response = "Tidak ada jawaban."
    st.text_area("Jawaban Chatbot:", chat_response, height=150)

st.markdown("---")

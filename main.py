
##keenam
import os
import requests
import streamlit as st
from dotenv import load_dotenv
import dashscope
from dashscope import Generation  # Pastikan sudah diinstall dengan `pip install dashscope`

# Load API key dari .env
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY tidak ditemukan di .env!")

# Set API key ke dashscope
dashscope.api_key = api_key

# Inisialisasi saldo e-wallet
saldo_ewallet = 0  
HARGA_SAMPAH_PLASTIK_PER_KG = 5000  # Harga per kg dalam rupiah
PLASTIK_BERAT_GRAM = 50  # Berat plastik per item dalam gram

# Streamlit UI
st.title("Sampah Bercuan - Klasifikasi Sampah")
st.write("Upload gambar sampah untuk dikategorikan.")

uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

def categorize_image(file_path):
    """Upload image & categorize using Qwen-VL"""
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

        if response is None or "output" not in response:
            return "Tidak diketahui"
        
        return response["output"]["text"]

    except Exception as e:
        return f"Error: {str(e)}"

def chatbot_response(category):
    """Chatbot response using Qwen-Max"""
    try:
        response = Generation.call(
            model="qwen-max",
            messages=[{"role": "user", "content": f"Apa manfaat dari sampah kategori {category}?"}]
        )

        if "output" in response:
            return response["output"]["text"]
        return "Tidak ada jawaban."

    except Exception as e:
        return f"Error: {str(e)}"

def hitung_deposit(category):
    """Cek apakah sampah plastik, lalu tambahkan saldo"""
    global saldo_ewallet  # Pastikan menggunakan variabel global
    if "plastik" in category.lower():
        tambahan_saldo = (PLASTIK_BERAT_GRAM / 1000) * HARGA_SAMPAH_PLASTIK_PER_KG
        saldo_ewallet += tambahan_saldo
        return f"Saldo e-wallet bertambah Rp{tambahan_saldo:.2f}. Total saldo: Rp{saldo_ewallet:.2f}"
    return "Tidak ada saldo yang ditambahkan."

def chatbot_investasi():
    """Chatbot investasi untuk menggunakan saldo e-wallet"""
    try:
        response = Generation.call(
            model="qwen-max",
            messages=[{"role": "user", "content": "Bagaimana cara saya menginvestasikan saldo e-wallet?"}]
        )

        if "output" in response:
            return response["output"]["text"]
        return "Tidak ada saran investasi."

    except Exception as e:
        return f"Error: {str(e)}"

if uploaded_file is not None:
    st.image(uploaded_file, caption="Gambar yang diupload", use_container_width=True)

    # Simpan file sementara
    img_path = f"temp_{uploaded_file.name}"
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Deteksi kategori sampah
    category = categorize_image(img_path)
    st.write(f"Kategori Sampah: {category}")

    # Hitung saldo jika plastik
    saldo_info = hitung_deposit(category)
    st.write(saldo_info)

    # Chatbot memberikan informasi tentang manfaat sampah
    chat_response = chatbot_response(category)
    st.write(f"Manfaat Sampah: {chat_response}")

    # Menu investasi
    if st.button("Gunakan Saldo untuk Investasi"):
        investasi_response = chatbot_investasi()
        st.write(f"💰 Saran Investasi: {investasi_response}")








# ## ke lima
# import os
# import requests
# import streamlit as st
# from dotenv import load_dotenv
# import dashscope
# from dashscope import Generation  # Pastikan sudah diinstall dengan `pip install dashscope`

# # Load API key dari .env
# load_dotenv()
# api_key = os.getenv("API_KEY")

# if not api_key:
#     raise ValueError("API_KEY tidak ditemukan di .env!")

# # Set API key ke dashscope
# dashscope.api_key = api_key

# # Streamlit UI
# st.title("Sampah Bercuan - Klasifikasi Sampah")
# st.write("Upload gambar sampah untuk dikategorikan.")

# uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

# def categorize_image(file_path):
#     """Upload image & categorize using Qwen-VL"""
#     try:
#         response = Generation.call(
#             model="qwen-vl-plus",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "Apa kategori dari gambar ini?"},
#                         {"type": "image_url", "image_url": {"url": file_path}},
#                     ],
#                 }
#             ],
#         )

#         # Debug output
#         print("Response dari API:", response)
#         st.write("Response dari API:", response)

#         if response is None:
#             return "Gagal mendapatkan respons dari API."
#         if "output" not in response:
#             return "Respons tidak memiliki output yang diharapkan."

#         return response["output"]["text"]

#     except Exception as e:
#         return f"Error: {str(e)}"

# def chatbot_response(category):
#     """Chatbot response using Qwen-Max"""
#     try:
#         response = Generation.call(
#             model="qwen-max",
#             messages=[{"role": "user", "content": f"Apa manfaat dari sampah kategori {category}?"}]
#         )

#         # Debug output
#         print("Response dari API:", response)
#         st.write("Response dari API:", response)

#         if response is None:
#             return "Gagal mendapatkan respons dari API."
#         if "output" not in response:
#             return "Respons tidak memiliki output yang diharapkan."

#         return response["output"]["text"]

#     except Exception as e:
#         return f"Error: {str(e)}"
        

# def chatbot_response(category):
#     """Chatbot response using Qwen-Max"""
#     try:
#         response = Generation.call(
#             model="qwen-max",
#             messages=[{"role": "user", "content": f"Apa manfaat dari sampah kategori {category}?"}]
#         )

#         if "output" in response:
#             return response["output"]["text"]
#         return "Tidak ada jawaban."

#     except Exception as e:
#         return f"Error: {str(e)}"

# if uploaded_file is not None:
#     #st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
#     st.image(uploaded_file, caption="Gambar yang diupload", use_container_width=True)

#     # Simpan file sementara
#     img_path = f"temp_{uploaded_file.name}"
#     with open(img_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Deteksi kategori sampah
#     category = categorize_image(img_path)
#     st.write(f"Kategori Sampah: {category}")

#     # Chatbot memberikan informasi tentang manfaat sampah
#     chat_response = chatbot_response(category)
#     st.write(f"Manfaat Sampah: {chat_response}")






# ##kekempat 
# import os
# import requests
# import streamlit as st
# from dotenv import load_dotenv

# # Load API key dari .env
# load_dotenv()
# API_KEY = os.getenv("API_KEY")

# if not API_KEY:
#     st.error("API Key tidak ditemukan! Pastikan sudah diset di .env dengan nama API_KEY")
#     st.stop()

# # API Base URL (Pastikan ini sesuai dokumentasi terbaru)
# API_BASE_URL = "https://dashscope.aliyuncs.com/v1"

# def categorize_image(file_path):
#     """Upload image & categorize using Qwen-VL"""
#     url = f"{API_BASE_URL}/services/aigc/text-to-image/generation"

#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     with open(file_path, "rb") as image_file:
#         files = {"file": image_file}
#         response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         return response.json().get("category", "Unknown")
#     else:
#         return f"Error {response.status_code}: {response.json()}"

# def chatbot_response(category):
#     """Chatbot response using Qwen-Max"""
#     url = f"{API_BASE_URL}/services/aigc/text-generation/generation"

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     prompt = f"Apa manfaat dari sampah kategori {category}?"
#     payload = {
#         "model": "qwen-max",
#         "messages": [{"role": "user", "content": prompt}]
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 200:
#         return response.json().get("message", "No response")
#     else:
#         return f"Error {response.status_code}: {response.json()}"

# # Streamlit UI
# st.title("Sampah Bercuan - Deteksi Kategori Sampah")
# st.write("Upload gambar sampah untuk dikategorikan.")

# uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
#     st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)

#     # Simpan file sementara
#     img_path = f"temp_{uploaded_file.name}"
#     with open(img_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Deteksi kategori sampah
#     category = categorize_image(img_path)
#     st.write(f"Kategori Sampah: {category}")

#     # Chatbot memberikan informasi tentang kategori sampah
#     chat_response = chatbot_response(category)
#     st.write(f"Manfaat Sampah: {chat_response}")






# ##ketiga
# import os
# import requests
# import streamlit as st
# from dotenv import load_dotenv

# # Load API key dari .env file
# load_dotenv()
# API_KEY = os.getenv("API_KEY")

# if not API_KEY:
#     st.error("API Key tidak ditemukan! Pastikan sudah diset di .env dengan nama API_KEY")
#     st.stop()

# # Base URL untuk Alibaba DashScope API
# API_BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1/apps/4f0f74ce308a435c86613251d38fcf21/completion"

# def categorize_image(file_path):
#     """Upload image & categorize using Qwen-VL"""
#     url = f"{API_BASE_URL}/vision_interpretation"
    
#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     with open(file_path, "rb") as image_file:
#         files = {"file": image_file}
#         response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         return response.json().get("category", "Unknown")
#     else:
#         return f"Error {response.status_code}: {response.json()}"

# def chatbot_response(category):
#     """Chatbot response using Qwen-Max"""
#     url = f"{API_BASE_URL}/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     prompt = f"Apa manfaat dari sampah kategori {category}?"
#     payload = {
#         "model": "qwen-max",
#         "messages": [{"role": "user", "content": prompt}]
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 200:
#         response_data = response.json()
#         return response_data.get("message", "No response")
#     else:
#         return f"Error {response.status_code}: {response.json()}"

# # Streamlit UI
# st.title("Sampah Bercuan - Deteksi Kategori Sampah")
# st.write("Upload gambar sampah untuk dikategorikan.")

# uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
#     st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)

#     # Simpan file sementara
#     img_path = f"temp_{uploaded_file.name}"
#     with open(img_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # Deteksi kategori sampah
#     category = categorize_image(img_path)
#     st.write(f"Kategori Sampah: {category}")

#     # Chatbot memberikan informasi tentang kategori sampah
#     chat_response = chatbot_response(category)
#     st.write(f"Manfaat Sampah: {chat_response}")








# # # ##kedua
# # # import os
# # # import requests
# # # from dotenv import load_dotenv
# # # import streamlit as st
# # # from openai import OpenAI
 

# # # # Load environment variables
# # # load_dotenv()
# # # api_key = os.getenv("API_KEY")
# # # print(f"API_KEY: {api_key}")  # Debugging
# # # if api_key:
# # #     os.environ["DASHSCOPE_API_KEY"] = api_key
# # # else:
# # #     raise ValueError("API_KEY tidak ditemukan di .env!")

# # # # Base URL for Alibaba DashScope API
# # # API_BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1/apps/4f0f74ce308a435c86613251d38fcf21/completion"

# # # Initialize DashScope client
# # client = DashScope()


# # def categorize_image(file_path):
# #     """Upload image & categorize using Qwen-VL"""
# #     model = "qwen-vl-plus"
# #     url = f"{API_BASE_URL}/vision_interpretation"

# #     headers = {
# #         "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"
# #     }

# #     with open(file_path, "rb") as image_file:
# #         files = {"file": image_file}
# #         response = requests.post(url, headers=headers, files=files)

# #     if response.status_code == 200:
# #         return response.json().get("category", "Unknown")
# #     else:
# #         return f"Error {response.status_code}: {response.json()}"


# # def chatbot_response(category):
# #     """Chatbot response using Qwen-Max"""
# #     model = "qwen-max"
# #     url = f"{API_BASE_URL}/chat/completions"

# #     headers = {
# #         "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
# #         "Content-Type": "application/json"
# #     }

# #     prompt = f"Apa manfaat dari sampah kategori {category}?"
# #     payload = {
# #         "model": model,
# #         "messages": [{"role": "user", "content": prompt}]
# #     }

# #     response = requests.post(url, headers=headers, json=payload)

# #     if response.status_code == 200:
# #         response_data = response.json()
# #         print(response_data)  # Debugging
# #         return response_data.get("message", "No response")
# #     else:
# #         return f"Error {response.status_code}: {response.json()}"


# # def main():
# #     file_path = "test_image.jpg"  # Ganti dengan path gambar yang diupload
# #     category = categorize_image(file_path)
# #     print(f"Kategori: {category}")

# #     chat_response = chatbot_response(category)
# #     print(f"Chatbot: {chat_response}")


# # if __name__ == "__main__":
# #     main()



# # ##pertama
# # # import os
# # # import requests
# # # from dotenv import load_dotenv
# # # import streamlit as st
# # # from openai import OpenAI
# # # from http.client import HTTPMessage
# # # from dashscope import DashScope


# # # # Load environment variables
# # # load_dotenv()
# # # os.environ["DASHSCOPE_API_KEY"] = os.getenv("API_KEY")

# # # # Base URL for Alibaba DashScope API
# # # API_BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1/apps/4f0f74ce308a435c86613251d38fcf21/completion"

# # # # Initialize DashScope client
# # # client = DashScope()


# # # def categorize_image(file_path):
# # #     """Upload image & categorize using Qwen-VL"""
# # #     model = "qwen-vl-plus"
# # #     url = f"{API_BASE_URL}/vision_interpretation"

# # #     headers = {
# # #         "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
# # #         "Content-Type": "multipart/form-data"
# # #     }

# # #     files = {"file": open(file_path, "rb")}

# # #     response = requests.post(url, headers=headers, files=files)

# # #     if response.status_code == 200:
# # #         category = response.json().get("category", "Unknown")
# # #         return category
# # #     else:
# # #         return f"Error {response.status_code}: {response.json()}"


# # # def chatbot_response(category):
# # #     """Chatbot response using Qwen-Max"""
# # #     model = "qwen-max"
# # #     url = f"{API_BASE_URL}/chat/completions"

# # #     headers = {
# # #         "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
# # #         "Content-Type": "application/json"
# # #     }

# # #     prompt = f"Apa manfaat dari sampah kategori {category}?"
# # #     payload = {
# # #         "model": model,
# # #         "messages": [{"role": "user", "content": prompt}]
# # #     }

# # #     response = requests.post(url, headers=headers, json=payload)

# # #     if response.status_code == 200:
# # #         return response.json().get("message", "No response")
# # #     else:
# # #         return f"Error {response.status_code}: {response.json()}"


# # # def main():
# # #     file_path = "test_image.jpg"  # Ganti dengan path gambar yang diupload
# # #     category = categorize_image(file_path)
# # #     print(f"Kategori: {category}")

# # #     chat_response = chatbot_response(category)
# # #     print(f"Chatbot: {chat_response}")


# # # if __name__ == "__main__":
# # #     main()

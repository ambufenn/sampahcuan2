import os
import requests
import streamlit as st
from dotenv import load_dotenv
import streamlit.components.v1 as components
from dashscope import Generation  # 确保它使用 pip install dashscope 安装

# 从 .env 加载 API 密钥
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("在 .env 中找不到API_KEY！")

# 将 API 密钥设置为 dashscope
dashscope.api_key = api_key

# 加载 UI 的 HTML 文件
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 在 Streamlit 中渲染 HTML
components.html(html_content, height=700)

# 图像分类功能
def categorize_image(file_path):
    """上传图片并使用Qwen-VL进行分类"""
    try:
        response = Generation.call(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "这张图片的分类是什么？"},
                        {"type": "image_url", "image_url": {"url": file_path}},
                    ],
                }
            ],
        )

        if response and "output" in response:
            return response["output"]["text"]
        return "Failed to get category."

    except Exception as e:
        return f"错误：{str(e)}"

# 聊天机器人的函数
def chatbot_response(category):
    """使用 Qwen-Max 的聊天机器人响应"""
    try:
        response = Generation.call(
            model="qwen-max",
            messages=[{"role": "user", "content": f"垃圾分类 {category} 有什么好处？"}]
        )

        if response and "output" in response:
            return response["output"]["text"]
        return "No answer."

    except Exception as e:
        return f"错误：{str(e)}"

# 处理文件上传
uploaded_file = st.file_uploader("选择图像...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="上传的图片", use_container_width=True)

    # 保存临时文件
    img_path = f"temp_{uploaded_file.name}"
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 检测垃圾类别
    category = categorize_image(img_path)
    st.write(f"垃圾桶类别： {category}")

    # 聊天机器人提供有关废物的好处的信息
    chat_response = chatbot_response(category)
    st.write(f"垃圾福利： {chat_response}")


# import os
# import requests
# import streamlit as st
# import streamlit.components.v1 as components
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

# # Load HTML file untuk UI
# with open("index.html", "r", encoding="utf-8") as f:
#     html_content = f.read()

# # Render HTML di Streamlit
# components.html(html_content, height=700)

# # Fungsi untuk klasifikasi gambar
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

#         if response and "output" in response:
#             return response["output"]["text"]
#         return "Gagal mendapatkan kategori."

#     except Exception as e:
#         return f"Error: {str(e)}"

# # Fungsi untuk chatbot

# def chatbot_response(category):
#     """Chatbot response using Qwen-Max"""
#     try:
#         response = Generation.call(
#             model="qwen-max",
#             messages=[{"role": "user", "content": f"Apa manfaat dari sampah kategori {category}?"}]
#         )
        
#         if response and "output" in response:
#             return response["output"]["text"]
#         return "Tidak ada jawaban."

#     except Exception as e:
#         return f"Error: {str(e)}"

# # Handle file upload
# uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
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






# # import os
# # import streamlit as st
# # from dotenv import load_dotenv
# # import dashscope
# # from dashscope import Generation  

# # # Load API key dari .env
# # load_dotenv()
# # api_key = os.getenv("API_KEY")

# # if not api_key:
# #     raise ValueError("API_KEY tidak ditemukan di .env!")

# # # Set API key ke dashscope
# # dashscope.api_key = api_key

# # # --- Fungsi untuk membaca HTML ---
# # def load_html(file_path):
# #     with open(file_path, "r", encoding="utf-8") as f:
# #         return f.read()

# # # Menampilkan HTML di Streamlit
# # html_path = "index.html"  # Sesuaikan dengan lokasi file
# # st.components.v1.html(load_html(html_path), height=600, scrolling=True)

# # # --- Fungsi Klasifikasi Sampah ---
# # def categorize_image(image_path):
# #     try:
# #         response = Generation.call(
# #             model="qwen-vl-plus",
# #             messages=[
# #                 {
# #                     "role": "user",
# #                     "content": [
# #                         {"type": "text", "text": "Apa kategori dari gambar ini?"},
# #                         {"type": "image_url", "image_url": {"url": image_path}},
# #                     ],
# #                 }
# #             ],
# #         )
# #         if response and "output" in response:
# #             return response["output"]["text"]
# #         return "Tidak diketahui"
# #     except Exception as e:
# #         return f"Error: {str(e)}"

# # # --- Fungsi Upload Gambar ---
# # uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "png", "jpeg"])

# # if uploaded_file:
# #     st.image(uploaded_file, caption="Gambar yang diupload", use_column_width=True)
    
# #     img_path = f"temp_{uploaded_file.name}"
# #     with open(img_path, "wb") as f:
# #         f.write(uploaded_file.getbuffer())

# #     category = categorize_image(img_path)

# #     # Update tampilan HTML dengan kategori sampah
# #     update_html = f"""
# #     <script>
# #         document.getElementById("kategori").innerText = "{category}";
# #     </script>
# #     """
# #     st.components.v1.html(update_html, height=10)

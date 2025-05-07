import streamlit as st
import requests
import time

st.set_page_config(page_title="Chatbot Admin Prodi", page_icon="🎓")
st.title("🎓 Chatbot Admin Prodi")

# Inisialisasi histori chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan seluruh pesan sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari pengguna
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Tambahkan pesan user ke histori
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tempatkan respons asisten di bawahnya
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("Sedang mengetik jawaban..."):
            try:
                # Kirim ke endpoint API Colab kamu
                response = requests.post(
                    "https://your-ngrok-api-url.ngrok.io/chat",  # Ganti URL ini
                    json={"prompt": prompt},
                    timeout=30
                )
                answer = response.json().get("response", "⚠️ Tidak ada jawaban.")
            except Exception as e:
                answer = f"⚠️ Gagal menghubungi API: {e}"

        # Efek ketikan per huruf
        for char in answer:
            full_response += char
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
        message_placeholder.markdown(full_response)

    # Tambahkan respons asisten ke histori
    st.session_state.messages.append({"role": "assistant", "content": full_response})

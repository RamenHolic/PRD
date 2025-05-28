import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

SYSTEM_PROMPT = (
    "Kamu adalah asisten AI ahli di bidang asuransi kesehatan. "
    "Jawablah pertanyaan pengguna secara akurat, jelas, dan sopan. "
    "Jika pertanyaan tidak terkait asuransi, tolak secara sopan."
)

# Histori percakapan
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

st.title("🤖 Chatbot Asuransi (Ollama + Streamlit)")

user_input = st.text_input("Tanyakan tentang asuransi kesehatan:")

if st.button("Kirim") and user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "messages": st.session_state.history, "stream": False}
    )
    if response.status_code == 200:
        reply = response.json()["message"]["content"]
        st.session_state.history.append({"role": "assistant", "content": reply})
        st.success(reply)
    else:
        st.error("❌ Gagal menghubungi Ollama. Pastikan sudah dijalankan.")

# Menampilkan histori
if st.checkbox("Tampilkan histori percakapan"):
    for msg in st.session_state.history:
        if msg["role"] != "system":
            st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
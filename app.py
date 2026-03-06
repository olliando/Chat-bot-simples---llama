import streamlit as st
from openai import OpenAI

ia = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

st.title("🤖 Robozinho do Oliver")

if "lista_mensagens" not in st.session_state:
    st.session_state.lista_mensagens = []

for msg in st.session_state.lista_mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem aqui...", key="unique_chat_input"):
    st.session_state.lista_mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = ia.chat.completions.create(
            model="llama3.2:3b",  # mude pra :1b se travar
            messages=st.session_state.lista_mensagens,
            temperature=0.7,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.lista_mensagens.append({"role": "assistant", "content": full_response})
    st.rerun()
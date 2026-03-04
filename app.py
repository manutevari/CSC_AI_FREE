import streamlit as st
from mas_engine import ask_ai

st.set_page_config(page_title="CSC AI Assistant")

st.title("CSC AI Knowledge Assistant")

question = st.text_input("Ask a question")

if question:
    with st.spinner("Thinking..."):
        answer = ask_ai(question)

    st.write(answer)

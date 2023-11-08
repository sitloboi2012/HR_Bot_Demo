# -*- coding: utf-8 -*-
import streamlit as st

from app.src.convo_bot import HRBot
from app.constant import LLM_MODEL, LANGCHAIN_VECTOR_DB

BOT = HRBot(LANGCHAIN_VECTOR_DB, llm_model=LLM_MODEL)

st.title("Candidate Pages")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = BOT.response_query(prompt)
        message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

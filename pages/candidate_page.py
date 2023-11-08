# -*- coding: utf-8 -*-
import streamlit as st

from app.src.convo_bot import HRBot
from app.constant import LLM_MODEL, LANGCHAIN_VECTOR_DB
from app.model.prompt_template import GREETING_TEMPLATE

BOT = HRBot(LANGCHAIN_VECTOR_DB, llm_model=LLM_MODEL)
BOT.initialize_agent()

st.title("Candidate Pages")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown(GREETING_TEMPLATE)
    st.session_state.messages.append({"role": "assistant", "content": GREETING_TEMPLATE})


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response, intermediate_step = BOT.generate_response(prompt)
        message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

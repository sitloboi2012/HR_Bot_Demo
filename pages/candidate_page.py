# -*- coding: utf-8 -*-
import streamlit as st

from app.src.convo_bot import HRBot
from app.constant import LLM_MODEL_3, LANGCHAIN_VECTOR_DB, RETRIEVAL_CHAIN
from app.model.prompt_template import GREETING_TEMPLATE

BOT = HRBot(LANGCHAIN_VECTOR_DB, llm_model=LLM_MODEL_3)
BOT.setup_bm25()
BOT.ensemble_search_docs()

st.title("Candidate Pages")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# with st.chat_message("assistant"):
#    message_placeholder = st.empty()
#    message_placeholder.markdown(GREETING_TEMPLATE)
#    st.session_state.messages.append({"role": "assistant", "content": GREETING_TEMPLATE})


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = BOT.generate_response(prompt)
        message_placeholder.markdown(response["answer"])
        # st.write(response["source_documents"])
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        # st.session_state.messages.append({"role": "assistant", "content": sources_document})

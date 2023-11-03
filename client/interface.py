# -*- coding: utf-8 -*-
from __future__ import annotations
import os

import streamlit as st


# from client.partials import material_sidebar
from app.src.document_loader import PDFDocumentLoader, WordDocumentLoader
from app.src.convo_bot import HRBot
from app.constant import LLM_MODEL, LANGCHAIN_VECTOR_DB

LOADER_FUNC = {
    ".pdf": PDFDocumentLoader(text_splitter=None),
    ".docx": WordDocumentLoader(text_splitter=None),
    ".doc": WordDocumentLoader(text_splitter=None),
}

BOT = HRBot(LANGCHAIN_VECTOR_DB, llm_model=LLM_MODEL)


def process_document(file_content: bytes, file_name: str, file_extension: str) -> bool | ValueError:
    if file_extension not in LOADER_FUNC:
        raise ValueError(f"{file_extension} is not supported")

    docs = LOADER_FUNC[file_extension].load_document(file_content, file_name)
    LOADER_FUNC[file_extension].upload_to_db(docs)

    return True


def main_interface():
    st.title("HR ChatBot")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "docx", "doc"], accept_multiple_files=True)
    if uploaded_file is not None:
        for data in uploaded_file:
            bytes_data, data_name, extension = data.getvalue(), data.name, os.path.splitext(data.name)[1]
            process_document(bytes_data, data_name, extension)

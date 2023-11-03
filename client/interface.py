# -*- coding: utf-8 -*-
from __future__ import annotations

import streamlit as st
import chromadb

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


# from client.partials import material_sidebar
from app.src.document_loader import PDFDocumentLoader

VECTOR_DB = chromadb.PersistentClient(path="database/vectordb")
# collection = vectordb.get_or_create_collection(name="test")
EMBEDDING_FUNC = OpenAIEmbeddings(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model_name="text-embedding-ada-002",
)

LANGCHAIN_VECTOR_DB = Chroma(client=VECTOR_DB, collection_name="test", embedding_function=EMBEDDING_FUNC)

PDF_LOADER = PDFDocumentLoader(vector_db=LANGCHAIN_VECTOR_DB, embedding_model=EMBEDDING_FUNC, text_splitter=None)


def main_interface():
    st.title("HR ChatBot")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)
    if uploaded_file is not None:
        for data in uploaded_file:
            bytes_data = data.getvalue()
            st.write("Read Document")
            docs = PDF_LOADER.load_document(bytes_data, data.name)
            st.write("Push to DB")
            PDF_LOADER.upload_to_db(docs)
            st.write("Done")

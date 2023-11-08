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
    try:
        st.success(f"Successfully add {file_name} on to the database")
    except Exception:
        st.error(f"Cannot upload {file_name} to the database")
    return True


def visualize_all_document():
    current_db_info = LANGCHAIN_VECTOR_DB.get()
    document_list = {i["filename"] for i in current_db_info["metadatas"]}

    st.write(f"- There are __{len(current_db_info['ids'])} documents__ in the database.")

    if len(document_list) == 0:
        st.markdown("- There is no document in the database")
    else:
        st.markdown(
            f"""
                - Name of document that is uploaded:
                __{document_list}__
                """
        )
    # st.write(LANGCHAIN_VECTOR_DB.get())


def search_docs(query_input):
    return LANGCHAIN_VECTOR_DB.similarity_search(query_input, k=2)


def main_interface():
    st.title("HR Page")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "docx", "doc"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded_file is not None:
        st.markdown(
            """
        <style>
            .uploadedFile {display: none}
        <style>""",
            unsafe_allow_html=True,
        )
        for data in uploaded_file:
            bytes_data, data_name, extension = data.getvalue(), data.name, os.path.splitext(data.name)[1]
            process_document(bytes_data, data_name, extension)

    with st.form(key="search_docs_form"):
        query = st.text_input("Search for a document: ")
        if search := st.form_submit_button("Seach"):  # noqa: F841
            st.write(search_docs(query))
    visualize_all_document()


main_interface()

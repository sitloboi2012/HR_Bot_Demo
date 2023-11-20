# -*- coding: utf-8 -*-
from __future__ import annotations
import os

import streamlit as st

from app.src.document_loader import PDFDocumentLoader, WordDocumentLoader
from app.src.convo_bot import HRBot
from app.constant import LLM_MODEL_3, LANGCHAIN_VECTOR_DB
from app.src.utils import chunking_job_description, convert_to_document

LOADER_FUNC = {
    ".pdf": PDFDocumentLoader(text_splitter=None),
    ".docx": WordDocumentLoader(text_splitter=None),
    ".doc": WordDocumentLoader(text_splitter=None),
}

BOT = HRBot(LANGCHAIN_VECTOR_DB, llm_model=LLM_MODEL_3)


VECTORDB_RETRIEVER = LANGCHAIN_VECTOR_DB.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 4, "score_threshold": 0.3},
)


def process_document(file_content: bytes, file_name: str, file_extension: str) -> bool | ValueError:
    if file_extension not in LOADER_FUNC:
        raise ValueError(f"{file_extension} is not supported")

    docs = LOADER_FUNC[file_extension].load_document(file_content, file_name)
    # raw_result = chunking_job_description(docs)
    # clean_docs = convert_to_document(raw_result, file_name, file_name)
    LOADER_FUNC[file_extension].upload_to_db([docs])
    try:
        st.success(f"Successfully add {file_name} on to the database")
    except Exception:
        st.error(f"Cannot upload {file_name} to the database")
    return True


def visualize_all_document():  # sourcery skip: simplify-len-comparison
    current_db_info = LANGCHAIN_VECTOR_DB.get()
    document_list = {i["source"] for i in current_db_info["metadatas"]}

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


def search_docs(query, db):
    threshold_score = 0.6
    relevant_docs = db.similarity_search_with_relevance_scores(query)
    return [document for document in relevant_docs if document[1] >= threshold_score]


def upload_docs_to_db(list_of_docs, session_state):
    if session_state:
        for data in list_of_docs:
            bytes_data, data_name, extension = (
                data.getvalue(),
                data.name,
                os.path.splitext(data.name)[1],
            )
            process_document(bytes_data, data_name, extension)


def main_interface():
    st.title("HR Page")

    if "upload" not in st.session_state:
        st.session_state.upload = False

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "docx", "doc"], accept_multiple_files=True)
    if uploaded_file is not None:
        st.session_state.upload = True
        upload_docs_to_db(uploaded_file, st.session_state.upload)

    with st.form(key="search_docs_form"):
        st.session_state.upload = False
        query = st.text_input("Search for a document: ")
        if search := st.form_submit_button("Seach"):  # noqa: F841
            st.write(search_docs(query, LANGCHAIN_VECTOR_DB))
    # visualize_all_document()


main_interface()

# -*- coding: utf-8 -*-
import streamlit as st
import chromadb

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.model.prompt_template import RETRIEVAL_TEMPLATE
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

LLM_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo-16k",
    temperature=0.2,
    openai_api_key="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",
    max_tokens=8000,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    n=2,
)

RETRIEVAL_PROMPT = PromptTemplate(
    template=RETRIEVAL_TEMPLATE,
    input_variables=["company_name", "company_background", "roles", "question", "context"],
)

EMBEDDING_FUNC = OpenAIEmbeddings(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model_name="text-embedding-ada-002",
)

LANGCHAIN_VECTOR_DB = Chroma(
    client=chromadb.PersistentClient(path="database/vectordb"),
    collection_name="test",
    embedding_function=EMBEDDING_FUNC,
)

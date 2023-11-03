# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.constant import LLM_MODEL
from app.model.prompt_template import RETRIEVAL_TEMPLATE
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


class HRBot:
    def __init__(self, vector_db: Any, llm_model: ChatOpenAI = LLM_MODEL):
        self.vector_db = vector_db
        self.llm_model = llm_model
        self.retriever = self.vector_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.5, "k": 2, "fetch_k": 10},
        )
        self.retrieval_prompt = ChatPromptTemplate.from_template(RETRIEVAL_TEMPLATE)

    def embed_query(self, query):
        return self.embedding_model.embed_query(query)

    def search_docs(self, query_input, embedding_func):
        return self.vector_db.similarity_search_by_vector(embedding_func.embed_query(query_input), k=2)

    def init_chain(self, query_input):
        pass

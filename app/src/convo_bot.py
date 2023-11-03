# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from app.constant import LLM_MODEL, RETRIEVAL_PROMPT


class HRBot:
    def __init__(self, vector_db: Any, llm_model: ChatOpenAI = LLM_MODEL):
        self.vector_db = vector_db
        self.llm_model = llm_model
        self.retriever = self.vector_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.5, "k": 2, "fetch_k": 10},
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            LLM_MODEL,
            retriever=self.retriever,
            chain_type_kwargs={"prompt": RETRIEVAL_PROMPT},
            return_source_documents=True,
        )

    def embed_query(self, query):
        return self.embedding_model.embed_query(query)

    def search_docs(self, query_input, embedding_func):
        return self.vector_db.similarity_search_by_vector(embedding_func.embed_query(query_input), k=2)

    def get_response(self, query):
        return self.qa_chain({"question": query, "company_name": "SmartDev", "company_background": "Beautiful and nice", "roles": "Software Engineer", "context": None})

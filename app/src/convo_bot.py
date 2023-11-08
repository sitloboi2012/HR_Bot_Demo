# -*- coding: utf-8 -*-
from __future__ import annotations
from functools import lru_cache
from typing import Any

from langchain.chat_models import ChatOpenAI
from app.constant import LLM_MODEL, RETRIEVAL_CHAIN, EMBEDDING_FUNC, RETRIEVAL_PROMPT
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from app.model.prompt_template import RETRIEVAL_TEMPLATE_2
from langchain.agents import Tool, initialize_agent
from langchain.schema.output_parser import OutputParserException


class HRBot:
    def __init__(self, vector_db: Any, llm_model: ChatOpenAI = LLM_MODEL):
        self.vector_db = vector_db
        self.llm_model = llm_model
        self.retriever = self.vector_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.5, "k": 2, "fetch_k": 10},
        )
        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=5,
            return_messages=True,
            output_key="output",
        )

    @lru_cache
    def initialize_agent(self) -> None:
        """
        Initializes the bot agent.

        """
        retriever_chain = RetrievalQA.from_chain_type(
            LLM_MODEL,
            retriever=self.retriever,
            chain_type_kwargs={"prompt": RETRIEVAL_PROMPT},
        )
        tools = [
            Tool(
                name="Document Search",
                func=retriever_chain.run,
                description="useful for when you need to find answer for question that have information from the document or related to the document.",
            )
        ]
        self.agent = initialize_agent(
            agent="chat-conversational-react-description",
            tools=tools,
            llm=LLM_MODEL,
            verbose=True,
            max_iterations=2,
            early_stopping_method="generate",
            memory=self.conversational_memory,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

    def search_docs(self, query_input, embedding_func):
        return self.vector_db.similarity_search_by_vector(embedding_func.embed_query(query_input), k=1)

    def response_query(self, query: str):
        related_docs = self.search_docs(query, EMBEDDING_FUNC)
        return RETRIEVAL_CHAIN.run(
            {
                "company_name": "SmartDev",
                "hiring_role": related_docs,
                "question": query,
            }
        )

    def generate_response(self, query: str) -> str:
        """
        Generates a response to the user query.

        Args:
            query (str): The user query.

        Returns:
            str: The generated response.

        """
        try:
            response = self.agent(query)
        except OutputParserException:  # used for handle could not parse llm output error
            return "The query / prompt is a little bit unclear, can you help me evaluate it more ?"

        return response["output"], response["intermediate_steps"]

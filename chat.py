# -*- coding: utf-8 -*-
import chainlit as cl
import chromadb

from typing import Dict, Any

from chainlit import Message
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from app.model.prompt_template import GREETING_TEMPLATE
from app.constant import RETRIEVAL_PROMPT
from langchain.prompts import PromptTemplate


class AnswerConversationBufferMemory(ConversationBufferMemory):
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        return super(AnswerConversationBufferMemory, self).save_context(inputs, {"response": outputs["answer"]})


EMBEDDING_FUNC = OpenAIEmbeddings(
    openai_api_key="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",
    model_name="text-embedding-ada-002",
)

LANGCHAIN_VECTOR_DB = Chroma(
    client=chromadb.PersistentClient(path="database/vectordb"),
    collection_name="test",
    embedding_function=EMBEDDING_FUNC,
)

LLM_MODEL_4 = ChatOpenAI(
    model_name="gpt-4-1106-preview",
    temperature=0.2,
    openai_api_key="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",
    # frequency_penalty=0.5,
    # presence_penalty=0.5,
    streaming=True,
)

CONDENSE_PROMPT = """Given the following conversation and a follow up question,
rephrase the follow up question to be a standalone question using the information from chat history.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(CONDENSE_PROMPT)


MEMORY = AnswerConversationBufferMemory(memory_key="chat_history", return_messages=True)
RETRIEVER = LANGCHAIN_VECTOR_DB.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 4, "score_threshold": 0.3})
chain_qa = ConversationalRetrievalChain.from_llm(
    llm=LLM_MODEL_4,
    retriever=RETRIEVER,
    condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    chain_type="stuff",
    condense_question_llm=LLM_MODEL_4,
    memory=MEMORY,
    combine_docs_chain_kwargs={"prompt": RETRIEVAL_PROMPT},
    return_source_documents=True,
)


@cl.on_chat_start
async def start_message():
    await Message(content=f"{GREETING_TEMPLATE}").send()


@cl.on_message
async def main(message: cl.Message):
    # response = chain_qa({"question": message.content})
    # response = await chain_qa.acall({"question": message.content},
    #                                callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True)])
    # await cl.Message(
    #    content = f"{response['answer']}",
    #    elements = response["source_documents"]
    # ).send()
    res = await chain_qa.acall(message.content, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True)])
    answer = res["answer"]

    if answer.startswith("I don't know"):
        answer = "Pinging HR now ..."
        await cl.Message(content=answer).send()
    else:
        text_elements = []

        if source_documents := res["source_documents"]:
            for source_doc in source_documents:
                source_name = f"{source_doc.metadata['source']} - {source_doc.metadata['information']}"
                # source_name = f"Source: {source_doc.metadata['source']} - {source_doc.metadata['information']} "
                # Create the text element referenced in the message
                text_elements.append(cl.Text(content=source_doc.page_content, name=source_name))
            if source_names := [text_el.name for text_el in text_elements]:
                answer += f"\nSources: {', '.join(source_names)}"
            else:
                answer += "\nNo sources found"

        await cl.Message(content=answer, elements=text_elements).send()

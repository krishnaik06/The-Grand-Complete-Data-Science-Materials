from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

def build_qa_chain(vector_store):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=512
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = PromptTemplate.from_template(
        """You are an AI assistant helping users find information from their documents.

Using the context below, provide a clear and accurate answer to the question.

Guidelines:
- Answer directly based on the context when the information is available
- If the context doesn't contain the answer but the question is general knowledge, provide a helpful response and note it's not from the documents
- If the question requires specific information from the documents that isn't present, state: "I don't have enough information in the provided documents to answer this question."

Context:
{context}

Question: {question}

Answer:"""
    )

    # LCEL pipeline (no deprecated imports)
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever

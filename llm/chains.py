# app/llm/chains.py
from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from sqlalchemy.orm import Session

from llm.client import get_chat_model
from llm.prompts import RAG_PROMPT
from rag.retrievers import get_base_retriever


def build_rag_chain():
    """
    Create a simple RAG chain:
    1. Take a question.
    2. Use retriever to fetch context docs.
    3. Stuff them into a prompt.
    4. Ask the LLM to answer.
    """
    llm = get_chat_model()
    retriever = get_base_retriever()

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    rag_chain = (
        {
            "question": RunnablePassthrough(),
            "context": retriever | format_docs,
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return rag_chain


def answer_question_with_rag(
    question: str,
    db: Session,
) -> Dict[str, Any]:
    """
    Simple wrapper: run RAG and return a response dict.
    (db is not used yet here, but we keep it for future SQL+RAG logic.)
    """
    rag_chain = build_rag_chain()
    answer = rag_chain.invoke(question)
    return {"answer": answer}

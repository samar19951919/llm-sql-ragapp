# app/llm/prompts.py
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are a helpful assistant for a movie rental database (Sakila-like).
You can answer questions using:
- Natural language context from a vector database (descriptions of films, actors, etc.).
- Numerical / factual data from SQL queries when provided.

Always:
- Explain your reasoning in simple terms.
- When you mention numeric facts (payments, counts, etc.) try to tie them back to the user question.
"""

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            "Question: {question}\n\n"
            "Context from documents:\n{context}\n\n"
            "Answer in a concise, friendly way.",
        ),
    ]
)

# api/routes_chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.chat import ChatRequest, ChatResponse
from llm.chains import answer_question_with_rag

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat_endpoint(
    payload: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    """
    Main chat endpoint.

    - Takes a natural language question from the client.
    - Uses the RAG chain to answer, which internally:
        * calls the vector retriever over pgvector
        * uses the ingested film/customer/actor docs as context
    """
    result = answer_question_with_rag(payload.question, db=db)
    return ChatResponse(answer=result["answer"])

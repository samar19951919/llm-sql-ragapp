# app/main.py
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import configure_logging
from app.api.routes_chat import router as chat_router
from app.api.routes_admin import router as admin_router

def create_app() -> FastAPI:

    configure_logging()

    app = FastAPI(
        title="LLM RAG App",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router, prefix="/chat", tags=["chat"])
    app.include_router(admin_router, prefix="/admin", tags=["admin"])

    @app.get("/", response_class=HTMLResponse)
    def index():
        return """
        <!doctype html>
        <html>
        <head>
          <title>RAG Chatbot</title>
        </head>
        <body>
          <h1>RAG Chatbot</h1>
          <textarea id="question" rows="4" cols="60"
            placeholder="Type your question..."></textarea><br>
          <button onclick="send()">Ask</button>
          <pre id="answer"></pre>

          <script>
            async function send() {
              const q = document.getElementById('question').value;
              const res = await fetch('/chat/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: q})
              });
              const data = await res.json();
              document.getElementById('answer').textContent = data.answer || JSON.stringify(data);
            }
          </script>
        </body>
        </html>
        """

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app



app = create_app()

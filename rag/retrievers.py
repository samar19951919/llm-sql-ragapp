from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
from langchain_community.document_compressors import LLMLinguaCompressor
from app.core.configs import settings
from langchain_core.vectorstores import VectorStoreRetriever
from app.db.vectorstore import get_vectorstore


# now gedeclaring the base retriever

def get_base_retriever() -> VectorStoreRetriever:

    vs = get_vectorstore()

    return vs.as_retriever(kwargs=3)

#b noew declaring the m,ethod to get the 


def get_compressed_retriver() -> ContextualCompressionRetriever:

    #more fancier retriver that first retrives then use llm to compress the coontext

    llm = ChatOpenAI(model = settings.CHAT_MODEL)
    compressor = LLMLinguaCompressor.from_llm(llm)
    base = get_base_retriever()
    return ContextualCompressionRetriever(base_retriever = base,compressor = compressor)


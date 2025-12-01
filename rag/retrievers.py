from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
from langchain_community.document_compressors import LLMLinguaCompressor
from langchain_core.vectorstores import VectorStoreRetriever

from core.configs import settings
from db.vectorstore import get_vectorstore


# now declaring the base retriever

def get_base_retriever() -> VectorStoreRetriever:
    vs = get_vectorstore()
    return vs.as_retriever(search_kwargs={"k": 3})


# now declaring the method to get the compressed retriever

def get_compressed_retriver() -> ContextualCompressionRetriever:
    # more fancier retriever that first retrieves then use llm to compress the context

    llm = ChatOpenAI(model=settings.CHAT_MODEL)
    compressor = LLMLinguaCompressor.from_llm(llm)
    base = get_base_retriever()
    return ContextualCompressionRetriever(base_retriever=base, compressor=compressor)

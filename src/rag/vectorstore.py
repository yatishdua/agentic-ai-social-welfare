from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def build_policy_vectorstore(docs):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

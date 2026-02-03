from rag.loader import load_policy_docs
from rag.vectorstore import build_policy_vectorstore


def load_policy_rag():
    docs = load_policy_docs("data/policy_docs")
    return build_policy_vectorstore(docs)

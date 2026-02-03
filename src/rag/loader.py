from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path


def load_policy_docs(path: str):
    docs = []
    for file in Path(path).glob("*.md"):
        loader = TextLoader(str(file))
        doc = loader.load()
        for d in doc:
            d.metadata["source"] = file.name
        docs.extend(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )

    return splitter.split_documents(docs)

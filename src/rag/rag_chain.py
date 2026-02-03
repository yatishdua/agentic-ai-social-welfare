from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from rag.prompt import RAG_PROMPT


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def answer_policy_question(vectorstore, question: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    docs = retriever.invoke(
        f"{question}"
    )

    if not docs:
        return {
            "answer": "I cannot find this information in the policy documents.",
            "sources": []
        }

    context = "\n\n".join(d.page_content for d in docs)

    response = llm.invoke(
        [
            SystemMessage(
                content=RAG_PROMPT.format(
                    context=context,
                    question=question
                )
            )
        ]
    )

    sources = [
        {
            "source": d.metadata.get("source", "unknown"),
            "excerpt": d.page_content[:200] + "..."
        }
        for d in docs
    ]

    return {
        "answer": response.content,
        "sources": sources
    }

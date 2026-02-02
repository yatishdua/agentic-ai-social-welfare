import yaml
from src.utils.path_utils import project_path

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama


def load_llm():
    with open(project_path("src", "config", "policy.yaml")) as f:
        policy = yaml.safe_load(f)

    llm_cfg = policy["llm"]
    provider = llm_cfg["provider"]
    temperature = llm_cfg.get("temperature", 0)

    # -------------------------
    # OpenAI (BEST for structure)
    # -------------------------
    if provider == "openai":
        return ChatOpenAI(
            model=llm_cfg["model"]["openai"],
            temperature=temperature
        )

    # -------------------------
    # Ollama (local)
    # -------------------------
    if provider == "ollama":
        return ChatOllama(
            model=llm_cfg["model"]["ollama"],
            temperature=temperature
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")

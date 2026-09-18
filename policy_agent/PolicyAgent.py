"""Policy-grounded LangChain agent."""

from importlib import import_module
from pathlib import Path
import re
from typing import Any

from langchain.agents import create_agent

from .config import Settings
from .retrieval import PolicyRetriever
from .safety import SafetyGuard


SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "system_prompt.txt"


def load_system_prompt() -> str:
    """Load the editable response guideline used by the language model."""

    try:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RuntimeError(f"System prompt file is unavailable: {SYSTEM_PROMPT_PATH}") from exc


def ensure_source_citation(answer: str, messages: list[Any]) -> str:
    """Keep grounded answers and attach sources returned by the retrieval tool."""

    sources = []
    for message in messages:
        content = str(getattr(message, "content", ""))
        sources.extend(re.findall(r"\[Source:[^\]]+\]", content))

    unique_sources = list(dict.fromkeys(sources))
    if unique_sources:
        answer = re.sub(r"\bSource:\s*none\.?", "", answer, flags=re.IGNORECASE).strip()
        if "[Source:" in answer:
            return answer
        return f"{answer.rstrip()} {' '.join(unique_sources)}"

    if "[Source:" in answer:
        return answer

    return "The provided policy documents do not contain enough information to answer that question."


class PolicyAgent:
    """Coordinate safety checks and the retrieval-grounded language model."""

    def __init__(self, vector_store: Any, settings: Settings):
        try:
            chat_ollama = import_module("langchain_ollama").ChatOllama
        except (ImportError, AttributeError) as exc:
            raise RuntimeError(
                "langchain-ollama is required; install project dependencies first."
            ) from exc

        self._agent = create_agent(
            model=chat_ollama(model=settings.chat_model, temperature=0),
            system_prompt=load_system_prompt(),
        )
        self._retriever = PolicyRetriever(vector_store, settings)

    def answer(self, question: str) -> tuple[str, list[Any]]:
        refusal = SafetyGuard.refusal_for(question)
        if refusal:
            return refusal, []

        retrieved_context = self._retriever.search(question)
        grounded_question = (
            f"User question:\n{question}\n\n"
            f"Retrieved policy context:\n{retrieved_context}"
        )
        result = self._agent.invoke(
            {"messages": [{"role": "user", "content": grounded_question}]}
        )
        answer = result["messages"][-1].content
        answer = ensure_source_citation(answer, result["messages"])

        tool_calls = []
        for message in result["messages"]:
            tool_calls.extend(getattr(message, "tool_calls", None) or [])
        return answer, tool_calls

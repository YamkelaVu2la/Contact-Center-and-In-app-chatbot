# Contact-Center-and-In-app-chatbot

A local, policy-grounded customer support assistant using Ollama, LangChain, and ChromaDB.

## Project layout

```text
policy_agent/
  PolicyAgent.py  # PolicyAgent and strict grounding prompt
  cli.py         # InteractiveCLI
  config.py      # Settings and project paths
  knowledge.py   # Document loading and vector-store construction
  prompts/
    system_prompt.txt  # Editable response rules for the language model
  retrieval.py   # Relevance-filtered retrieval tool
  safety.py      # Prompt-injection and sensitive-data guards
agent.py         # Backward-compatible launcher
knowledge/       # Policy source documents
chroma_db/       # Local vector-store persistence
```

## Run

1. Install dependencies: `python -m pip install -r requirements.txt`
2. Start Ollama and ensure `qwen2.5:latest` and `nomic-embed-text:latest` are available.
3. Run: `python agent.py`

# Policy Corpus Agent

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

## Run locally after cloning

### Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/download) installed and running

### Windows PowerShell

1. Clone the repository and enter the project directory:

  ```powershell
  git clone https://github.com/YamkelaVu2la/Contact-Center-and-In-app-chatbot.git
  cd Contact-Center-and-In-app-chatbot
  ```

2. Create and activate a virtual environment:

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

3. Install the Python dependencies:

  ```powershell
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  ```

4. Download the local chat and embedding models:

  ```powershell
  ollama pull qwen2.5:latest
  ollama pull nomic-embed-text:latest
  ```

  Make sure Ollama is running before starting the agent.

5. Start the assistant:

  ```powershell
  python agent.py
  ```

6. Ask questions about the policies in `knowledge/`. Type `exit` to stop.

The application creates the local ChromaDB vector store in `chroma_db/` when it starts. That directory is generated locally and is excluded from Git.
"""Command-line interface for the policy assistant."""

from .PolicyAgent import PolicyAgent
from .config import Settings
from .knowledge import KnowledgeBase


class InteractiveCLI:
    """Run the interactive customer-question loop."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def run(self) -> None:
        print("Building vector store...")
        vector_store = KnowledgeBase(self.settings).build()
        print("Initializing agent...")
        agent = PolicyAgent(vector_store, self.settings)
        print("\nReady! Ask about company policies. Type 'exit' to quit.\n")

        while True:
            question = input("You: ").strip()
            if not question or question.lower() == "exit":
                return

            answer, tool_calls = agent.answer(question)
            for call in tool_calls:
                print(f"  [retrieving: {call['args'].get('query', '')}]")
            print(f"\nAgent: {answer}\n")
"""Compatibility launcher for the modular policy assistant."""

from policy_agent.cli import InteractiveCLI
from policy_agent.config import Settings
from policy_agent.safety import refusal_for


def main() -> None:
    InteractiveCLI(Settings.from_project_root()).run()


if __name__ == "__main__":
    main()